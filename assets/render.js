function createContentRenderer(elementId) {
    const element = document.getElementById(elementId)
    return (content, onAction = () => {}) => {
        if (content.type === "menu") {
            fixedRenderMenu(element, content, onAction)
        } else if (content.type === "map") {
            const menuContent = {
                type: "menu",
                actions: content.locations.map(location => ({
                    title: location.title,
                    ...location.action,
                })),
                background: content.background
            }
            fixedRenderMenu(element, menuContent, onAction)
        }
    }
}

function fixedRenderMenu(element, content, onAction) {
    const background = content.background
    const actions = [
        ...content.actions,
        ...(content.backAction ? [{
            id: "menu-back-action",
            title: "Back",
            ...content.backAction
        }] : [])
    ]
    const menuItems = actions.map(({title, id}) => `<div class="menu-item" id="${id}">${title}</div>`).join("")
    element.innerHTML = `<div class="menu-content" style="background-image: url('${background}')"><div class="menu">${menuItems}</div></div>`
    for (const action of actions) {
        const actionElement = document.getElementById(action.id)
        actionElement.addEventListener("click", () => {
            onAction(action)
        })
    }
}
