Vue.component("ge-action", {
    props: {
        title: {
            type: String,
            default: "Button"
        },
        id: {
            type: String,
            default: ""
        },
        type: {
            type: String,
            default: "navigate"
        },
        enabled: {
            type: Boolean,
            default: true
        },
        onAction: {
            type: Function,
            default() {}
        }
    },
    template: (
`
<div class="menu-item"
    :id="id"
    v-on:click="triggerAction"
    :class="{disabled: !enabled}"
>{{ title }}</div>
`
    ),
    computed: {
        triggerAction() {
            return () => {
                console.log("action:", this.id)
                this.onAction({id: this.id})
            }
        }
    }
})