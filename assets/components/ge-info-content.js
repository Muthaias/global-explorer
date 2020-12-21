Vue.component("ge-info-content", {
    props: {
        title: {
            type: String,
            default: "Hello world"
        },
        background: {
            type: String,
            default: "https://images.unsplash.com/photo-1538488881038-e252a119ace7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
        },
        titleImage: {
            type: String,
            default: "https://images.unsplash.com/photo-1604138808764-e873853af44e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1817&q=80"
        },
        content: {
            type: String,
            default: ``
        },
        actions: {
            type: Array,
            default() {return []}
        },
        contentTransform: {
            type: Function,
            default: function(c) {return c}
        },
        onAction: {
            type: Function,
            default() {}
        }
    },
    template: (
`
<div class="info-content" :style="backgroundStyle">
    <div class="info">
        <div class="header" :style="headerStyle">
            <div class="text">{{ title }}</div>
        </div>
        <div class="content" v-html="transformedContent"></div>
        <div class="footer">
            <ge-action
                v-for="action in actions"
                v-bind:key="action.id"
                v-bind:title="action.title"
                v-bind:id="action.id"
                v-bind:type="action.type"
                v-bind:enabled="action.enabled"
                v-bind:on-action="onAction"
            ></ge-action>
        </div>
    </div>
</div>
`
    ),
    computed: {
        backgroundStyle() {return `background-image: url('${this.background}')`},
        headerStyle() {return `background-image: url('${this.titleImage}')`},
        transformedContent() {return this.contentTransform(this.content)}
    }
})