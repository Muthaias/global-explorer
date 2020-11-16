function createContentRenderer(elementId) {
    const element = document.getElementById(elementId)
    return (content, onAction = () => {}) => {
        if (content.type === "menu") {
            const background = content.background;
            const menuItems = content.actions.map(({title, id}) => `<div class="menu-item" id="${id}">${title}</div>`).join("")
            element.innerHTML = `<div class="menu-content" style="background-image: url('${background}')"><div class="menu">${menuItems}</div></div>`
            for (const action of content.actions) {
                const actionElement = document.getElementById(action.id)
                actionElement.addEventListener("click", () => {
                    onAction(action)
                })
            }
        }
    }
}

