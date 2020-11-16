function createLog(elementId) {
    const element = document.getElementById(elementId)
    const log = []

    const combineEntries = (entries) => {
        return entries.map(entry => `<div>${entry}</div>`).join("")
    }
    return (...entries) => {
        log.push(entries)
        element.innerHTML = log.map(entries => `<div class="log-entry">${combineEntries(entries)}</div>`).join("")
    }
}