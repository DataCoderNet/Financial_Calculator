<template>
  <div class="fin-menu">
    <!-- Main FIN button -->
    <CalculatorButton
      v-if="!isMenuOpen"
      label="FIN"
      type="fin"
      @click="toggleMenu"
    />

    <!-- Menu Content -->
    <div v-if="isMenuOpen" class="menu-content">
      <!-- Main Categories Menu -->
      <div v-if="currentView === 'main'" class="main-menu">
        <div class="menu-header">
          <h3>Financial Functions</h3>
          <button class="close-button" @click="closeMenu">&times;</button>
        </div>
        <div class="menu-grid">
          <CalculatorButton
            v-for="category in categories"
            :key="category.key"
            :label="category.label"
            type="fin"
            @click="selectCategory(category)"
          />
        </div>
      </div>

      <!-- TVM Menu -->
      <TVMMenu
        v-else-if="currentView === 'tvm'"
        @back="currentView = 'main'"
        @select-function="selectFunction"
      />

      <!-- Parameter Input -->
      <div v-if="showParameterInput" class="parameter-input">
        <div class="parameter-header">
          <h4>{{ currentFunction.label }}: {{ currentParameter.label }}</h4>
          <button class="close-button" @click="cancelInput">&times;</button>
        </div>
        <div class="parameter-value">{{ parameterValue || '0' }}</div>
        <div class="parameter-description">
          {{ currentParameter.description }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CalculatorButton from './CalculatorButton.vue'
import TVMMenu from './menus/TVMMenu.vue'

export default {
  name: 'FinButtonMenu',
  components: {
    CalculatorButton,
    TVMMenu
  },
  data() {
    return {
      isMenuOpen: false,
      currentView: 'main',
      currentFunction: null,
      currentParameter: null,
      parameterValue: '',
      parameters: {},
      categories: [
        { key: 'tvm', label: 'TVM', description: 'Time Value of Money' },
        { key: 'icnv', label: 'ICNV', description: 'Interest Conversion' },
        { key: 'cflo', label: 'CFLO', description: 'Cash Flow' },
        { key: 'bond', label: 'BOND', description: 'Bond Calculations' },
        { key: 'deprc', label: 'DEPRC', description: 'Depreciation' },
        { key: 'bsch', label: 'BSCH', description: 'Business Schedules' }
      ]
    }
  },
  computed: {
    showParameterInput() {
      return this.currentFunction && this.currentParameter
    }
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen
      if (!this.isMenuOpen) {
        this.resetState()
      }
    },
    closeMenu() {
      this.isMenuOpen = false
      this.resetState()
    },
    resetState() {
      this.currentView = 'main'
      this.currentFunction = null
      this.currentParameter = null
      this.parameterValue = ''
      this.parameters = {}
    },
    selectCategory(category) {
      this.currentView = category.key
    },
    selectFunction(func) {
      this.currentFunction = func
      // For TVM functions, define the required parameters
      if (func.type === 'tvm') {
        this.parameters = {
          n: { label: 'N', description: 'Number of periods' },
          i: { label: 'I%YR', description: 'Annual interest rate (%)' },
          pv: { label: 'PV', description: 'Present value' },
          pmt: { label: 'PMT', description: 'Payment amount' },
          fv: { label: 'FV', description: 'Future value' }
        }
        // Start with the first parameter
        this.currentParameter = this.parameters[Object.keys(this.parameters)[0]]
      }
    },
    handleCalculatorInput(value) {
      if (this.showParameterInput) {
        this.parameterValue = value
      }
    },
    cancelInput() {
      this.currentFunction = null
      this.currentParameter = null
      this.parameterValue = ''
    },
    async calculateResult() {
      try {
        // TODO: Call the appropriate API endpoint based on currentFunction
        const result = await fetch(`/api/fin/tvm/${this.currentFunction.key}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.parameters)
        })
        const data = await result.json()
        // TODO: Display result
      } catch (error) {
        console.error('Calculation error:', error)
      }
    }
  }
}
</script>

<style scoped>
.fin-menu {
  position: relative;
  display: inline-block;
  z-index: 100;
}

.menu-content {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 5px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  min-width: 280px;
}

.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
}

.menu-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0 5px;
}

.close-button:hover {
  color: #333;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  padding: 10px;
}

.parameter-input {
  padding: 15px;
  border-top: 1px solid #eee;
}

.parameter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.parameter-header h4 {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.parameter-value {
  font-size: 1.5rem;
  text-align: right;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 10px;
}

.parameter-description {
  font-size: 0.9rem;
  color: #666;
  text-align: center;
}
</style>