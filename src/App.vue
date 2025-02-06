<!-- Keep template and style exactly as they were, only updating the handleAssignValue method in script -->
<script>
import CalculatorDisplay from './components/CalculatorDisplay.vue'
import CalculatorButton from './components/CalculatorButton.vue'
import FinButtonMenu from './components/FinButtonMenu.vue'

export default {
  name: 'App',
  components: {
    CalculatorDisplay,
    CalculatorButton,
    FinButtonMenu
  },
  data() {
    return {
      displayValue: '0',
      previousValue: null,
      operator: null,
      waitingForSecondOperand: false,
      error: '',
      // Financial calculation state
      isFinancialMode: false,
      currentParameter: null,
      calculatedParameter: '',
      inputDescription: '',
      finParameters: null,
      // Memory state
      memoryValue: 0
    }
  },
  methods: {
    // Memory Operations
    memoryAdd() {
      const currentValue = parseFloat(this.displayValue)
      if (!isNaN(currentValue)) {
        this.memoryValue += currentValue
      }
    },
    memorySubtract() {
      const currentValue = parseFloat(this.displayValue)
      if (!isNaN(currentValue)) {
        this.memoryValue -= currentValue
      }
    },
    memoryRecall() {
      this.displayValue = String(this.memoryValue)
      if (this.isFinancialMode && this.currentParameter) {
        this.$refs.finMenu.assignParameterValue(this.currentParameter, this.displayValue)
      }
    },
    memoryClear() {
      this.memoryValue = 0
    },
    handleInput(value) {
      if (this.isFinancialMode) {
        const newValue = this.displayValue === '0' ? value : this.displayValue + value
        this.displayValue = newValue
        return
      }
      this.appendDigit(value)
    },
    clearAll() {
      // Reset calculator display
      this.displayValue = '0'
      this.previousValue = null
      this.operator = null
      this.waitingForSecondOperand = false
      this.error = ''
      this.inputDescription = ''
      this.calculatedParameter = ''
      
      // Reset financial mode state
      this.isFinancialMode = false
      this.currentParameter = null

      // Reset all TVM parameters
      if (this.$refs.finMenu) {
        this.$refs.finMenu.resetState()
      }
    },
    appendDigit(digit) {
      if (this.waitingForSecondOperand) {
        this.displayValue = digit
        this.waitingForSecondOperand = false
      } else {
        this.displayValue = this.displayValue === '0' ? digit : this.displayValue + digit
      }
    },
    appendDecimal() {
      if (this.waitingForSecondOperand) {
        this.displayValue = '0.'
        this.waitingForSecondOperand = false
        return
      }
      if (!this.displayValue.includes('.')) {
        this.displayValue += '.'
      }
    },
    toggleSign() {
      const value = parseFloat(this.displayValue) * -1
      this.displayValue = String(value)
    },
    percentage() {
      const value = parseFloat(this.displayValue) / 100
      this.displayValue = String(value)
    },
    setOperator(nextOperator) {
      if (this.isFinancialMode) {
        if (nextOperator === '+' || nextOperator === '-') {
          this.toggleSign()
        }
        return
      }

      const value = parseFloat(this.displayValue)
      
      if (this.previousValue === null) {
        this.previousValue = value
      } else if (this.operator && !this.waitingForSecondOperand) {
        const result = this.performCalculation()
        this.displayValue = String(result)
        this.previousValue = result
      }

      this.waitingForSecondOperand = true
      this.operator = nextOperator
    },
    performCalculation() {
      const prev = this.previousValue
      const current = parseFloat(this.displayValue)
      
      if (isNaN(prev) || isNaN(current)) return current

      let result
      switch (this.operator) {
        case '+':
          result = prev + current
          break
        case '-':
          result = prev - current
          break
        case '*':
          result = prev * current
          break
        case '/':
          if (current === 0) {
            this.error = 'Cannot divide by zero'
            return 0
          }
          result = prev / current
          break
        default:
          return current
      }
      
      result = parseFloat(result.toFixed(10))
      return Number.isFinite(result) ? result : current
    },
    calculate() {
      if (!this.operator || this.waitingForSecondOperand) {
        return
      }

      const result = this.performCalculation()
      this.displayValue = String(result)
      this.previousValue = null
      this.operator = null
      this.waitingForSecondOperand = false
    },
    handleAssignValue(param) {
      // Store the value before updating the display
      const value = this.displayValue
      // Assign the current display value to the selected parameter
      this.isFinancialMode = true
      this.$refs.finMenu.assignParameterValue(param, value)
      // Update display description with the actual value
      this.inputDescription = `${param.label} = ${value}`
      // Reset display for next input
      this.displayValue = '0'
    },
    updateFinParameters(params) {
      this.finParameters = params
    },
    handleCalculationResult(result) {
      if (result) {
        this.displayValue = String(result.value)
        this.calculatedParameter = result.parameter.toUpperCase()
        this.inputDescription = `${this.calculatedParameter} = ${result.value}`
        this.error = ''
      }
    },
    handleMenuState(isOpen) {
      this.isFinancialMode = isOpen
      if (!isOpen) {
        this.calculatedParameter = ''
        this.inputDescription = ''
      }
    }
  }
}
</script>
