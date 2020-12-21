Vue.component("ge-credit-card", {
    props: {
        name: {
            type: String,
            default: "Guy Incognito"
        },
        number: {
            type: String,
            default: "1111 1111 1111 1111"
        },
        issuer: {
            type: String,
            default: "SHOWYA"
        },
        enabled: {
            type: Boolean,
            default: true
        },
        background: {
            type: String,
            default: "https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1834&q=80"
        }
    },
    template: (
`
<div class="credit-card" v-bind:class="{enabled}">
    <div class="name">{{name}}</div>
    <div class="number">{{number}}</div>
    <div class="chip"></div>
    <div class="logo">{{issuer}}</div>
</div>
`
    ),
    computed: {
        cardStyle() {return `background: url('${this.background}')`}
    }
})