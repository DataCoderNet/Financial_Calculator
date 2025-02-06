<template>
  <div class="app-container">
    <div class="calculator">
      <CalculatorDisplay
        :value="displayValue"
        :error="error"
        :description="inputDescription"
        :parameters="finParameters"
        :calculated-parameter="calculatedParameter"
        :is-financial-mode="isFinancialMode"
        :memory-active="!!memoryValue"
      />
      <!-- Memory buttons row -->
      <div class="memory-row">
        <CalculatorButton label="MC" type="memory" @click="memoryClear" />
        <CalculatorButton label="MR" type="memory" @click="memoryRecall" />
        <CalculatorButton label="M-" type="memory" @click="memorySubtract" />
        <CalculatorButton label="M+" type="memory" @click="memoryAdd" />
      </div>
      <!-- FIN button at the top -->
      <div class="fin-section">
        <FinButtonMenu 
          ref="finMenu" 
          @assign-value="handleAssignValue"
          @parameter-update="updateFinParameters"
          @calculation-request="handleCalculationResult"
          @menu-state="handleMenuState"
        />
      </div>
      <div class="calculator-grid">
        <!-- First row -->
        <CalculatorButton label="C" type="function" @click="clearAll" />
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
        // Always update display value in financial mode
        const newValue = this.displayValue === '0' ? value : this.displayValue + value
        this.displayValue = newValue
        return
      }

      // Normal calculator input handling
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
        // In financial mode, + and - are used for sign changes
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
      // Assign the current display value to the selected parameter
      this.isFinancialMode = true
      this.$refs.finMenu.assignParameterValue(param, this.displayValue)
      this.displayValue = '0'  // Reset display for next input
      this.inputDescription = `${param.label} = ${this.displayValue}`
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
      // Update financial mode based on menu state
      this.isFinancialMode = isOpen
      if (!isOpen) {
        this.calculatedParameter = ''
        this.inputDescription = ''
      }
    }
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 2rem;
  min-width: 320px;
  min-height: 100vh;
  background-color: #f0f0f0;
}

#app {
  margin: 0 auto;
  text-align: center;
}

.app-container {
  position: relative;
  width: fit-content;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding-top: 2rem;
}

.calculator {
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 320px;
  height: 680px; /* Increased height to accommodate expanded display */
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 2rem;
}

.memory-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 8px;
  margin-bottom: 8px;
}

.calculator-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 8px;
  flex: 1;
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
