class GlobalExplorer {
    constructor(api, onUpdate = () => {}, log = () => {}) {
        this._api = api
        this._player = null
        this._content = {}
        this._version = "unknown"
        this._onUpdate = onUpdate
        this._log = log
    }

    async init() {
        await this._update()
    }

    get player() {
        return this._player
    }

    get content() {
        return this._content
    }

    get version() {
        return this._version
    }

    async doAction(action) {
        await this._api.action(action)
        await this._update()
    }

    async _update() {
        this._player = (await this._api.player())
        this._content = await this._api.content()
        this._version = await this._api.version()
        this._onUpdate()
    }
}