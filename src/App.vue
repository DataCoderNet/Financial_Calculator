<template>
  <div class="calculator">
    <CalculatorDisplay
      :value="displayValue"
      :error="error"
    />
    <div class="calculator-grid">
      <!-- First row -->
      <CalculatorButton label="C" type="function" @click="clear" />
      <CalculatorButton label="±" type="function" @click="toggleSign" />
      <CalculatorButton label="%" type="function" @click="percentage" />
      <CalculatorButton label="÷" type="operator" @click="setOperator('/')" :is-active="operator === '/'" />

      <!-- Second row -->
      <CalculatorButton label="7" type="digit" @click="handleInput('7')" />
      <CalculatorButton label="8" type="digit" @click="handleInput('8')" />
      <CalculatorButton label="9" type="digit" @click="handleInput('9')" />
      <CalculatorButton label="×" type="operator" @click="setOperator('*')" :is-active="operator === '*'" />

      <!-- Third row -->
      <CalculatorButton label="4" type="digit" @click="handleInput('4')" />
      <CalculatorButton label="5" type="digit" @click="handleInput('5')" />
      <CalculatorButton label="6" type="digit" @click="handleInput('6')" />
      <CalculatorButton label="−" type="operator" @click="setOperator('-')" :is-active="operator === '-'" />

      <!-- Fourth row -->
      <CalculatorButton label="1" type="digit" @click="handleInput('1')" />
      <CalculatorButton label="2" type="digit" @click="handleInput('2')" />
      <CalculatorButton label="3" type="digit" @click="handleInput('3')" />
      <CalculatorButton label="+" type="operator" @click="setOperator('+')" :is-active="operator === '+'" />

      <!-- Fifth row -->
      <CalculatorButton label="0" type="digit" @click="handleInput('0')" class="span-2" />
      <CalculatorButton label="." type="digit" @click="handleInput('.')" />
      <CalculatorButton label="=" type="operator" @click="calculate" />
    </div>
    <!-- FIN menu at the bottom -->
    <div class="fin-section">
      <FinButtonMenu ref="finMenu" @parameter-input="handleParameterInput" />
    </div>
  </div>
</template>

<script>
import CalculatorDisplay from './components/CalculatorDisplay.vue'
import CalculatorButton from './components/CalculatorButton.vue'
import FinButtonMenu from './components/FinButtonMenu.vue'

const API_BASE_URL = 'http://localhost:8000/api'

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
      currentFinancialFunction: null,
      financialParameters: {}
    }
  },
  methods: {
    handleInput(value) {
      if (this.isFinancialMode) {
        // If in financial mode, pass input to FIN menu
        this.$refs.finMenu.handleCalculatorInput(value)
        return
      }

      // Normal calculator input handling
      if (value === '.') {
        this.appendDecimal()
      } else {
        this.appendDigit(value)
      }
    },
    clear() {
      if (this.isFinancialMode) {
        // If in financial mode, reset financial state
        this.isFinancialMode = false
        this.currentFinancialFunction = null
        this.financialParameters = {}
      }
      this.displayValue = '0'
      this.previousValue = null
      this.operator = null
      this.waitingForSecondOperand = false
      this.error = ''
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
      this.displayValue = String(-parseFloat(this.displayValue))
    },
    percentage() {
      const currentValue = parseFloat(this.displayValue)
      
      if (this.operator && this.previousValue !== null) {
        // If we're in the middle of an operation, calculate percentage of the first number
        const percentValue = (currentValue / 100) * this.previousValue
        this.displayValue = String(percentValue)
      } else {
        // If no operation is in progress, just convert to percentage
        this.displayValue = String(currentValue / 100)
      }
      
      this.error = ''
    },
    setOperator(nextOperator) {
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
      
      // Format the result to prevent floating point issues
      result = parseFloat(result.toFixed(10))
      return Number.isFinite(result) ? result : current
    },
    calculate() {
      if (this.isFinancialMode) {
        this.calculateFinancial()
        return
      }

      if (!this.operator || this.waitingForSecondOperand) {
        return
      }

      const result = this.performCalculation()
      this.displayValue = String(result)
      this.previousValue = null
      this.operator = null
      this.waitingForSecondOperand = false
    },
    // Financial calculation methods
    handleParameterInput(paramData) {
      this.isFinancialMode = true
      this.currentFinancialFunction = paramData
      this.displayValue = '0'
      this.waitingForSecondOperand = false
    },
    async calculateFinancial() {
      if (!this.currentFinancialFunction) return

      try {
        const response = await fetch(`${API_BASE_URL}/fin/tvm/${this.currentFinancialFunction.key}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.financialParameters)
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Calculation failed')
        }

        const result = await response.json()
        this.displayValue = String(result.value)
        this.isFinancialMode = false
        this.currentFinancialFunction = null
        this.financialParameters = {}
      } catch (error) {
        this.error = error.message
        console.error('Financial calculation error:', error)
      }
    }
  }
}
</script>

<style>
body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
  background-color: #f0f0f0;
}

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.calculator {
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 280px;
  margin: 0 auto;
}

.calculator-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 8px;
}

.span-2 {
  grid-column: span 2;
}

.fin-section {
  margin-top: 12px;
  display: flex;
  justify-content: center;
}
</style>
