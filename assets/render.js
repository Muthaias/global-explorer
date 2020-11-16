function createContentRenderer(elementId, renderer = contentRenderer) {
    const element = document.getElementById(elementId)
    let lastContent = null
    return (content, onAction = () => {}) => {
        const contentCache = JSON.stringify(content)
        if (lastContent === contentCache) return

        lastContent = contentCache
        const onTransitionEnd = () => {
            renderer(element, content, onAction)
            element.removeEventListener("transitionend", onTransitionEnd);
            element.classList.add("visible")
        };
        element.addEventListener("transitionend", onTransitionEnd);
        element.classList.remove("visible")
    }
}

function contentRenderer(element, content, onAction) {
    if (content.type === "menu") {
        fixedRenderMenu(element, content, onAction)
    } else if (content.type === "map") {
        const menuContent = {
            type: "menu",
            title: content.title,
            actions: content.locations.map(location => ({
                title: location.title,
                ...location.action,
            })),
            background: content.background
        }
        fixedRenderMenu(element, menuContent, onAction)
    } else if (content.type === "info") {
        fixedRenderInfo(element, content, onAction)
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
    const title = content.title
    const menuItems = actions.map(renderButton).join("")
    const menuTitle = title ? `<div class="title">${title}</div>` : ""
    element.innerHTML = (
`
<div class="menu-content" style="background-image: url('${background}')">
    <div class="menu">${menuTitle + menuItems}</div>
</div>
`
    )
    connectActions(actions, onAction)
}

function fixedRenderInfo(element, content, onAction) {
    const {
        title,
        titleImage,
        markdown,
        background,
        finishAction
    } = content
    const finishButton = renderButton(finishAction)
    element.innerHTML = (
`
<div class="info-content" style="background-image: url('${background}')">
    <div class="info">
        <div class="header" style="background-image: url('${titleImage}')">${title}</div>
        <div class="content">${markdownToHTML(markdown)}</div>
        <div class="footer">${finishButton}</div>
    </div>
</div>
`
    )
    connectActions([content.finishAction], onAction)
}

function renderButton({title, id}) {
    return `<div class="menu-item" id="${id}">${title}</div>`
}

function markdownToHTML(markdown) {
    return markdown
}

function connectActions(actions, onAction) {
    for (const action of actions) {
        const actionElement = document.getElementById(action.id)
        actionElement.addEventListener("click", () => {
            onAction(action)
        })
    }
}

function createCreditCardControl(cardId, nameId, cardNumberId, accountBalanceId) {
    const [
        card,
        name,
        cardNumber,
        accountBalance
    ] = [cardId, nameId, cardNumberId, accountBalanceId].map(id => document.getElementById(id))

    let isOpen = false
    let currentBalance = 0
    let balanceInterval = null
    return (player) => {
        isOpen = !!player
        if (player) {
            name.innerHTML = player.name
            cardNumber.innerHTML = player.account.card_number
            if (balanceInterval !== null) {
                clearInterval(balanceInterval)
            }
            const numSteps = 10
            const balanceStep = (player.account.balance - currentBalance) / numSteps
            let currentStep = 0
            balanceInterval = setInterval(() => {
                currentBalance = currentBalance + balanceStep
                accountBalance.innerText = `Account balance: ${Math.round(currentBalance)}$`
                if (++currentStep === numSteps) {
                    currentBalance = player.account.balance
                    clearInterval(balanceInterval)
                    balanceInterval = null
                }
            }, 50)
        }
        if (isOpen) {
            card.classList.remove("closed")
        } else {
            card.classList.add("closed")
        }
    }
}