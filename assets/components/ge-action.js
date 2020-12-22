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
<span>
    <span class="menu-group"
        v-if="type === 'input'"
        :class="{disabled: !enabled}"
    >
        <input type="text" v-model="value" :placeholder="title">
        <div class="menu-item"
            v-on:click="triggerAction"
            :class="{disabled: !enabled}"
        >{{ title }}</div>
    </span>
    <div class="menu-item"
        v-else
        v-on:click="triggerAction"
        :class="{disabled: !enabled}"
    >{{ title }}</div>
</span>
`
    ),
    data() {
        return {
            value: "",
        }
    },
    computed: {
        triggerAction() {
            return () => {
                console.log("action:", this.id)
                if (this.type === "input") {
                    this.onAction({id: this.id, value: this.value})
                } else {
                    this.onAction({id: this.id})
                }
            }
        }
    }
})