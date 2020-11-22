function createContentRenderer(
    elementId,
    options = {
        markdownTransform: markdownToHTML,
        renderer: contentRenderer
    }
) {
    const {renderer = contentRenderer} = options
    const element = document.getElementById(elementId)
    let lastContent = null
    return (content, onAction = () => {}) => {
        const contentCache = JSON.stringify(content)
        if (lastContent === contentCache) return

        lastContent = contentCache
        const onTransitionEnd = () => {
            renderer(element, content, onAction, options)
            element.removeEventListener("transitionend", onTransitionEnd);
            element.classList.add("visible")
        };
        element.addEventListener("transitionend", onTransitionEnd);
        element.classList.remove("visible")
    }
}

function contentRenderer(element, content, onAction, options) {
    if (content.type === "menu") {
        fixedRenderMenu(element, content, onAction, options)
    } else if (content.type === "map") {
        const menuContent = {
            type: "menu",
            title: content.title,
            actions: [
                ...content.locations.map(location => ({
                    title: location.title,
                    ...location.action,
                })),
                ...(content.actions || [])
            ],
            background: content.background
        }
        fixedRenderMenu(element, menuContent, onAction, options)
    } else if (content.type === "info") {
        fixedRenderInfo(element, content, onAction, options)
    }
}

function fixedRenderMenu(element, content, onAction, options) {
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

function fixedRenderInfo(element, content, onAction, {markdownTransform}) {
    const {
        title,
        titleImage,
        markdown,
        background,
        actions
    } = content
    const actionButtons = actions.map(renderButton).join("")
    element.innerHTML = (
`
<div class="info-content" style="background-image: url('${background}')">
    <div class="info">
        <div class="header" style="background-image: url('${titleImage}')">
            <div class="text">${title}</div>
        </div>
        <div class="content">${markdownTransform(markdown)}</div>
        <div class="footer">${actionButtons}</div>
    </div>
</div>
`
    )
    connectActions(actions, onAction)
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

function createCreditCardControl(
    cardId,
    nameId,
    cardNumberId,
    cardIssuerId,
    accountBalanceId,
    dateId,
) {
    const [
        card,
        name,
        cardNumber,
        accountBalance,
        date,
        cardIssuer,
    ] = [
        cardId,
        nameId,
        cardNumberId,
        accountBalanceId,
        dateId,
        cardIssuerId,
    ].map(id => document.getElementById(id))

    let isOpen = false
    let currentBalance = 0
    let balanceInterval = null
    return (player, game) => {
        isOpen = !!player
        if (player) {
            name.innerHTML = player.name
            cardNumber.innerHTML = player.account.card_number
            cardIssuer.innerHTML = player.account.card_issuer
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
        console.log(game)
        if (game) {
            date.innerText = `Time: ${game.time}`
        }
        if (isOpen) {
            card.classList.remove("closed")
        } else {
            card.classList.add("closed")
        }
    }
}