RUN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
podman run -it -p 5000:5000 -p 3000:3000 -v ${RUN_DIR}/:/exec:z fedora:global-explorer