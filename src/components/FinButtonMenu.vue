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
        :current-parameter="currentParameter"
        :parameter-values="parameterValues"
        @back="currentView = 'main'"
        @select-parameter="selectParameter"
        @calculate-parameter="calculateParameter"
      />
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
  emits: ['input-ready', 'parameter-update', 'calculation-triggered'],
  data() {
    return {
      isMenuOpen: false,
      currentView: 'main',
      currentParameter: null,
      parameterValues: {
        n: '',
        i: '',
        pv: '',
        pmt: '',
        fv: '',
        pyr: '12',
        end: true
      },
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
      this.currentParameter = null
      this.parameterValues = {
        n: '',
        i: '',
        pv: '',
        pmt: '',
        fv: '',
        pyr: '12',
        end: true
      }
      this.$emit('parameter-update', this.parameterValues)
    },
    selectCategory(category) {
      this.currentView = category.key
      this.$emit('parameter-update', this.parameterValues)
    },
    selectParameter(param) {
      this.currentParameter = param
      this.$emit('input-ready', {
        key: param.key,
        currentValue: this.parameterValues[param.key] || ''
      })
    },
    async calculateParameter(param) {
      this.currentParameter = param
      this.$emit('calculation-triggered')
      const result = await this.calculate()
      if (result !== null) {
        this.parameterValues[param.key] = String(result)
        this.$emit('parameter-update', this.parameterValues)
      }
    },
    handleCalculatorInput(value) {
      if (this.currentParameter) {
        // Update the parameter value
        this.parameterValues[this.currentParameter.key] = value
        this.$emit('parameter-update', this.parameterValues)
      }
    },
    async calculate() {
      if (this.currentView !== 'tvm') return null

      // Apply cash flow sign convention
      const params = { ...this.parameterValues }
      
      // Convert values to numbers and apply sign convention
      if (params.pv) params.pv = -Number(params.pv) // Money paid out is negative
      if (params.fv) params.fv = Number(params.fv)  // Money received is positive
      if (params.pmt) params.pmt = -Number(params.pmt) // Payments made are negative
      if (params.i) params.i = Number(params.i)
      if (params.n) params.n = Number(params.n)

      // Determine which calculation to perform based on the current parameter
      const endpoint = this.currentParameter.key

      try {
        const response = await fetch(`http://localhost:8000/api/fin/tvm/${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(params)
        })

        if (!response.ok) {
          throw new Error('Calculation failed')
        }

        const result = await response.json()
        
        // Reverse sign convention for display if needed
        let displayValue = result.value
        if (endpoint === 'pv' || endpoint === 'pmt') {
          displayValue = -displayValue
        }

        return displayValue
      } catch (error) {
        console.error('Failed to calculate:', error)
        return null
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
  position: fixed;
  top: 2rem; /* Match body padding */
  right: calc(50% - 160px); /* Center calculator width (320/2) */
  margin-right: -360px; /* Position to the right of calculator */
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
</style>