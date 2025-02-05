<template>
  <div class="calculator-container">
    <div class="calculator">
      <CalculatorDisplay
        :value="displayValue"
        :error="error"
        :description="inputDescription"
        :parameters="finParameters"
      />
      <!-- Move FIN button above calculator grid -->
      <div class="fin-section">
        <FinButtonMenu 
          ref="finMenu" 
          @input-ready="handleParameterInput"
          @parameter-update="updateFinParameters"
          @calculate="handleCalculate"
        />
      </div>
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
        <CalculatorButton label="." type="digit" @click="appendDecimal" />
        <CalculatorButton label="=" type="operator" @click="calculate" />
      </div>
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
      currentParameter: null,
      inputDescription: '',
      finParameters: null
    }
  },
  methods: {
    handleInput(value) {
      if (this.isFinancialMode) {
        // If in financial mode, use the current display value
        const newValue = this.displayValue === '0' ? value : this.displayValue + value
        this.displayValue = newValue
        this.$refs.finMenu.handleCalculatorInput(newValue)
        return
      }

      // Normal calculator input handling
      this.appendDigit(value)
    },
    clear() {
      if (this.isFinancialMode) {
        this.$refs.finMenu.handleCalculatorInput('0')
      }
      this.displayValue = '0'
      this.previousValue = null
      this.operator = null
      this.waitingForSecondOperand = false
      this.error = ''
      this.inputDescription = ''
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
      if (this.isFinancialMode) {
        this.$refs.finMenu.handleCalculatorInput(this.displayValue)
      }
    },
    percentage() {
      const value = parseFloat(this.displayValue) / 100
      this.displayValue = String(value)
      if (this.isFinancialMode) {
        this.$refs.finMenu.handleCalculatorInput(this.displayValue)
      }
    },
    setOperator(nextOperator) {
      if (this.isFinancialMode) {
        // In financial mode, = is used to confirm parameter input
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
    handleParameterInput(param) {
      this.isFinancialMode = true
      this.currentParameter = param
      this.displayValue = param.currentValue || '0'
      this.inputDescription = `Enter ${param.key.toUpperCase()}`
    },
    updateFinParameters(params) {
      this.finParameters = params
    },
    async handleCalculate(result) {
      if (result !== null) {
        this.displayValue = String(result)
        this.isFinancialMode = false
        this.currentParameter = null
        this.inputDescription = ''
      }
    }
  }
}
</script>

<style>
body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
  background-color: #f0f0f0;
  padding: 2rem;
}

#app {
  max-width: 1280px;
  margin: 0 auto;
  text-align: center;
}

.calculator-container {
  display: inline-flex;
  gap: 20px;
  margin: 0 auto;
  align-items: flex-start;
}

.calculator {
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 320px;
  display: flex;
  flex-direction: column;
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
  margin-bottom: 12px;
  display: flex;
  justify-content: flex-start;
}
</style>
