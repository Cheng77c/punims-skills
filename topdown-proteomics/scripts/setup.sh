#!/usr/bin/env bash
# 在 Shrimp sandbox:装 bohr CLI(幂等)+ 落环境文件供后续 Bash source。
# sandbox 每次 Bash 是独立 shell,env 不跨调用持久化,故写 /bohr-workspace/.bohr_env,
# 之后每条命令开头 `source /bohr-workspace/.bohr_env`。
set -e

if ! command -v bohr >/dev/null 2>&1 && [ ! -x "$HOME/.bohrium/bohr" ]; then
  touch "$HOME/.bashrc" 2>/dev/null || true   # 官方装脚本会 grep/sed .bashrc,缺文件(root 家目录常无)会报噪声
  /bin/bash -c "$(curl -fsSL https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_linux_curl.sh)"
fi

# 镜像地址单一源:skill 根的 image.txt(版本迭代只改这一处)。临时换镜像在 submit 前命令级 export。
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMG_DEFAULT="$(cat "$HERE/../image.txt" 2>/dev/null | tr -d '[:space:]')"

mkdir -p /bohr-workspace
ENVF=/bohr-workspace/.bohr_env
# ★ 幂等保值:先载入已有 .bohr_env 把上次写好的值放回 shell,这样本次平台若没注入,
#   下面的 ${VAR:-...} 会保留旧值,而不是用空值把好值冲掉(重复 setup 不再清空 key/项目)。
[ -f "$ENVF" ] && . "$ENVF" 2>/dev/null || true
# 例外:IMAGE_ADDRESS 不保值。它的单一源是 image.txt——若沿用 .bohr_env 缓存的旧 tag,
# 会盖过 image.txt 更新(改了版本号却仍提交旧镜像)。每次以 image.txt 为准;临时换镜像在
# submit 前命令级 `IMAGE_ADDRESS=… python3 submit_pipeline.py`,不持久化到 .bohr_env。
IMAGE_ADDRESS="$IMG_DEFAULT"
# ACCESS_KEY(bohr CLI 读)与 BOHR_ACCESS_KEY(脚本/curl 读)同源同值:一次解析、两名都写。
# source .bohr_env 后两个名都带 key,agent 不必再手动 export ACCESS_KEY="$BOHR_ACCESS_KEY"
# (P2 摆弄断 key 的根因就是 .bohr_env 只写了 ACCESS_KEY、没写 BOHR_ACCESS_KEY)。
AK="${ACCESS_KEY:-${BOHR_ACCESS_KEY:-}}"
cat > "$ENVF" <<EOF
export PATH="\$HOME/.bohrium:\$PATH"
export OPENAPI_HOST=https://openapi.dp.tech
export TIEFBLUE_HOST=https://tiefblue.dp.tech
export ACCESS_KEY="${AK}"
export BOHR_ACCESS_KEY="${AK}"
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
