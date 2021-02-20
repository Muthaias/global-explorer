Vue.component("ge-menu-content", {
    props: {
        title: {
            type: String,
            default: ""
        },
        background: {
            type: String,
            default: "https://images.unsplash.com/photo-1538488881038-e252a119ace7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
        },
        actions: {
            type: Array,
            default() {return []}
        },
        onAction: {
            type: Function,
            default() {}
        },
        content: {
            type: String,
            default: ``
        },
        contentTransform: {
            type: Function,
            default: function(c) {return c}
        },
    },
    template: (
`
<div class="menu-content" :style="backgroundStyle">
    <div class="menu">
        <div class="info">
            <div class="title">{{title}}</div>
            <div class="content" v-html="transformedContent"></div>
        </div>
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
`
    ),
    computed: {
        backgroundStyle() {return `background-image: url('${this.background}')`},
        transformedContent() {return this.contentTransform(this.content)}
    }
})