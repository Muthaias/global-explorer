function createLog(elementId) {
    const element = document.getElementById(elementId)
    const log = []
    return (entry) => {
        log.push(entry)
        element.innerHTML = log.map(entry => `<div class="log-entry">${entry}</div>`).join("")
    }
}