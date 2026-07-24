#!/usr/bin/env bash
# 在 Shrimp sandbox:装 bohr CLI(幂等)+ 落环境文件供后续 Bash source。
# sandbox 每次 Bash 是独立 shell,env 不跨调用持久化,故写 /bohr-workspace/.bohr_env,
# 之后每条命令开头 `source /bohr-workspace/.bohr_env`。
set -e

# 判据只认规范路径 $HOME/.bohrium/bohr,不认"PATH 上有个叫 bohr 的东西"。
# 已经翻过车:agent 自己 ln -s lbg ~/.local/bin/bohr 之后,`command -v bohr` 就成立了,
# setup.sh 于是跳过安装,真 CLI 一直没装上,而 sandbox 跨轮不重置,这个假 bohr 会一直骗下去。
if [ ! -x "$HOME/.bohrium/bohr" ]; then
  touch "$HOME/.bashrc" 2>/dev/null || true   # 官方装脚本会 grep/sed .bashrc,缺文件(root 家目录常无)会报噪声
  /bin/bash -c "$(curl -fsSL https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_linux_curl.sh)"
fi

# 镜像地址单一源:skill 根的 image.txt(版本迭代只改这一处)。临时换镜像在 submit 前命令级 export。
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMG_DEFAULT="$(cat "$HERE/../image.txt" 2>/dev/null | tr -d '[:space:]')"

mkdir -p /bohr-workspace
ENVF=/bohr-workspace/.bohr_env
# ★ 幂等:只从旧 .bohr_env 抢救 PROJECT_ID(平台不注入它),**绝不 source 整个旧文件**。
#   曾经这里 `. "$ENVF"` 把旧文件整个载回来 —— 旧文件里的 key 可能是已轮换的坏值,
#   会把平台本 shell 新注入的 BOHR_ACCESS_KEY 冲掉,造成"用户给了新 key 仍旧失败"。
#   平台每个 shell 注入的 BOHR_ACCESS_KEY 是 key 的**唯一权威**,不从磁盘旧值恢复。
OLD_PID=""
[ -f "$ENVF" ] && OLD_PID="$(sed -n 's/^export PROJECT_ID="\(.*\)"$/\1/p' "$ENVF" 2>/dev/null | tail -1)"
PROJECT_ID="${PROJECT_ID:-$OLD_PID}"
# 例外:IMAGE_ADDRESS 不保值。它的单一源是 image.txt——若沿用 .bohr_env 缓存的旧 tag,
# 会盖过 image.txt 更新(改了版本号却仍提交旧镜像)。每次以 image.txt 为准;临时换镜像在
# submit 前命令级 `IMAGE_ADDRESS=… python3 submit_pipeline.py`,不持久化到 .bohr_env。
IMAGE_ADDRESS="$IMG_DEFAULT"
# key 处理:.bohr_env 里写**引用不写值**。
# 平台每个 shell 都注入 BOHR_ACCESS_KEY(实测);bohr CLI 只认 ACCESS_KEY 这个名字。
# 所以这里写两行 `${A:-$B}` 的**字面引用**(用 \$ 转义,写入时不展开),source 时才从
# 平台注入的 live 环境解析出真值 —— key 的明文值从不落进磁盘文件。
# 这修掉了旧版把 `export ACCESS_KEY="<明文32位>"` 写进 .bohr_env 的问题:那既是密钥落盘,
# 又踩平台脱敏盲区(明文进了文件却没被 redact)。改后两个名字在 source 后仍都带值,
# agent 不必手动桥接,bohr CLI 也照认。
AK="${BOHR_ACCESS_KEY:-${ACCESS_KEY:-}}"   # 自检以平台注入的 BOHR_ACCESS_KEY 为准;不写进文件
cat > "$ENVF" <<EOF
export PATH="\$HOME/.bohrium:\$PATH"
export OPENAPI_HOST=https://open.bohrium.com
export TIEFBLUE_HOST=https://tiefblue.dp.tech
export ACCESS_KEY="\${BOHR_ACCESS_KEY:-\$ACCESS_KEY}"
export BOHR_ACCESS_KEY="\${BOHR_ACCESS_KEY:-\$ACCESS_KEY}"
export PROJECT_ID="${PROJECT_ID:-}"
export IMAGE_ADDRESS="${IMAGE_ADDRESS:-$IMG_DEFAULT}"
export MACHINE_TYPE="${MACHINE_TYPE:-c16_m32_cpu}"
EOF
echo "wrote $ENVF"

export PATH="$HOME/.bohrium:$PATH"
bohr version >/dev/null 2>&1 && echo "bohr ready" || echo "WARN: bohr 未就绪"
command -v python3 >/dev/null 2>&1 || echo "WARN: 需要 python3"
if [ -n "${AK:-}" ]; then
  echo "ACCESS_KEY 已注入(ACCESS_KEY+BOHR_ACCESS_KEY 同值)"
else
  # 以前这里只 echo WARN 就继续(set -e 拦不住 || 分支),setup 报"成功"、退出码 0。
  # agent 于是一路往下走,直到 submit 才炸,而那时的报错和真因(没授权)已经完全脱钩。
  echo "ERROR: ACCESS_KEY 未注入,没有它后续每一步都会失败。" >&2
  echo "FIX:   先在平台上完成授权、重载 skill,再跑 setup.sh。" >&2
  echo "NEVER: 不要手写 .bohr_env,不要猜一个 key 填进去。" >&2
  exit 1
fi
[ -n "${PROJECT_ID:-}" ] && echo "PROJECT_ID=$PROJECT_ID" || echo "WARN: PROJECT_ID 未注入——对话中用户已明确的项目 ID 可直接 export PROJECT_ID=<id> 使用;未知才 AskUserInput 索取;勿凭空编造默认值"
