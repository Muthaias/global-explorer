function createLog(elementId) {
    const element = document.getElementById(elementId)
    const log = []
    let isOpen = false;
    element.classList.add("closed")

    const combineEntries = (entries) => {
        return entries.map(entry => `<div>${entry}</div>`).join("")
    }
    const renderLog = (log) => {
        const controlId = `log-control-${elementId}`
        const control = `<div class="log-control" id="${controlId}">console</div>`
        element.innerHTML = control + log.map(entries => `<div class="log-entry">${combineEntries(entries)}</div>`).join("")
        const controlElement = document.getElementById(controlId)
        controlElement.addEventListener("click", () => {
            isOpen = !isOpen
            if (isOpen) {
                element.classList.remove("closed")
            } else {
                element.classList.add("closed")
            }
        })
    }
    return {
        log: (...entries) => {
            log.push(entries)
            renderLog(log)
        },
        clearLog: () => {
            log.splice(0, log.length)
            renderLog(log)
        }
    }
}