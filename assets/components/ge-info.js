Vue.component("ge-info", {
    props: {
        title: {
            type: String,
            default: "Info"
        },
        value: {
            type: [String, Number],
            default: "-"
        }
    },
    template: (
`
<div class="info">{{ title }}: {{ viewValue }}</div>
`
    ),
    data() {return {
        viewValue: "",
        valueInterval: null
    }},
    watch: {
        value(value) {
            if (this.valueInterval !== null) {
                clearInterval(this.valueInterval)
                this.valueInterval = null
            }
            if (typeof value === "number") {
                const lastValue = typeof this.viewValue === "number" ? this.viewValue : 0
                this.viewValue = lastValue
                const numSteps = 10
                const valueStep = (value - lastValue) / numSteps
                let currentStep = 0
                this.valueInterval = setInterval(() => {
                    this.viewValue = this.viewValue + valueStep
                    if (++currentStep === numSteps) {
                        this.viewValue = value
                        clearInterval(this.valueInterval)
                        this.valueInterval = null
                    }
                }, 50)
            } else {
                this.viewValue = value
            }
        }
    }
})