IMAGE_SIZE='100x100'        
IMAGE_TYPE='png'            
IMAGE_COLOR='gray'          
FILTER_DIR='data/filter'  
log() 
{
    local now="$(date +%F%T)"
    local message="$@"
    echo "[${now}] ${message}" 2>&1
}
sizeof() 
{ 
    du "$1" | cut -f1; 
}

convert_image() 
{
    local image_orig="$1"
    local filename="${image_orig%.*}"
    local image_out="${filename}.${IMAGE_TYPE}"
    convert "${image_orig}" \
        -resize "${IMAGE_SIZE}" \
        -colorspace "${IMAGE_COLOR}" \
        "${image_out}"
    [ "${image_out}" != "${image_orig}" ] && rm "${image_orig}"
    echo "${image_out}"
}
main() 
{
    local images="$@"
    set -o errexit
    set -o nounset
    set -o pipefail
    mkdir -p "${FILTER_DIR}"
    for image_orig in ${images}; do
        if [ $(sizeof "${image_orig}") -le 12 ]; then
            mv "${image_orig}" "${FILTER_DIR}"
            log "Remove auto-generated default avatar ${image_orig} to ${FILTER_DIR}"
        else
            local image_out="$(convert_image ${image_orig})"
            log "converted ${image_orig} to ${image_out}"
        fi
    done
}
main "$@"