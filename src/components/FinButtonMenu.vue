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
        @back="goBack"
        @select-parameter="assignToParameter"
        @calculation-request="handleCalculate"
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
  emits: ['assign-value', 'parameter-update', 'calculation-request', 'menu-state'],
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
      // Don't set financial mode when just opening the menu
      if (!this.isMenuOpen) {
        this.$emit('menu-state', false)
      }
    },
    closeMenu() {
      this.isMenuOpen = false
      this.$emit('menu-state', false)
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
      // Only set financial mode when selecting a specific function
      this.$emit('menu-state', true)
    },
    goBack() {
      this.currentView = 'main'
      // Return to normal display when going back to main menu
      this.$emit('menu-state', false)
    },
    assignToParameter(param) {
      this.$emit('assign-value', param)
    },
    assignParameterValue(param, value) {
      this.parameterValues[param.key] = value
      this.$emit('parameter-update', this.parameterValues)
    },
    async handleCalculate() {
      // Find which parameter is missing
      const missingParam = this.findMissingParameter()
      if (!missingParam) return

      this.currentParameter = {
        key: missingParam,
        label: this.getParameterLabel(missingParam)
      }
      
      try {
        const result = await this.calculate()
        if (result) {
          // Update the UI with the calculated result
          this.parameterValues[result.parameter] = String(result.value)
          this.$emit('parameter-update', this.parameterValues)
          // Trigger calculation completion
          this.$emit('calculation-request', result)
        }
      } catch (error) {
        console.error('Calculation failed:', error)
      }
    },
    getParameterLabel(key) {
      const labels = {
        n: 'N',
        i: 'I%YR',
        pv: 'PV',
        pmt: 'PMT',
        fv: 'FV'
      }
      return labels[key] || key.toUpperCase()
    },
    findMissingParameter() {
      const params = this.parameterValues
      const requiredParams = ['n', 'i', 'pv', 'pmt', 'fv']
      
      // Count filled parameters
      const filledParams = requiredParams.filter(param => 
        params[param] !== '' && params[param] !== undefined
      ).length

      // We need exactly 4 parameters filled to calculate the 5th
      if (filledParams !== 4) return null

      // Return the empty parameter
      return requiredParams.find(param => 
        !params[param] || params[param] === ''
      )
    },
    async calculate() {
      if (this.currentView !== 'tvm') return null

      // Filter out empty values and prepare parameters
      const params = Object.entries(this.parameterValues).reduce((acc, [key, value]) => {
        // Include non-empty values and always include pyr and end
        if (value !== '' && value !== undefined) {
          // Apply sign convention and convert to number if needed
          if (key === 'pv' || key === 'pmt') {
            acc[key] = -Number(value) // Money paid out is negative
          } else if (key === 'fv' || key === 'i' || key === 'n') {
            acc[key] = Number(value)  // Convert to number
          } else {
            acc[key] = value  // Keep as is for pyr and end
          }
        }
        return acc
      }, {})

      try {
        const response = await fetch(`http://localhost:8000/api/fin/tvm/${this.currentParameter.key}`, {
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
        if (this.currentParameter.key === 'pv' || this.currentParameter.key === 'pmt') {
          displayValue = -displayValue
        }

        return {
          value: displayValue,
          parameter: this.currentParameter.key
        }
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
  top: 50%; /* Center vertically */
  right: calc(50% - 160px); /* Center calculator width (320/2) */
  margin-right: -360px; /* Position to the right of calculator */
  transform: translateY(-50%); /* Adjust for vertical centering */
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  min-width: 280px;
  max-height: 80vh;
  overflow-y: auto;
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