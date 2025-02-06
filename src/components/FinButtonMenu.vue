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
    <transition name="menu">
      <div v-if="isMenuOpen" class="menu-content">
        <!-- Main Categories Menu -->
        <transition name="fade" mode="out-in">
          <div v-if="currentView === 'main'" class="main-menu" key="main">
            <div class="menu-header">
              <h3>Financial Functions</h3>
              <button class="close-button" @click="closeMenu">&times;</button>
            </div>
            <div class="menu-grid">
              <transition-group name="category">
                <CalculatorButton
                  v-for="category in categories"
                  :key="category.key"
                  :label="category.label"
                  type="fin"
                  @click="selectCategory(category)"
                />
              </transition-group>
            </div>
          </div>

          <!-- TVM Menu -->
          <TVMMenu
            v-else-if="currentView === 'tvm'"
            key="tvm"
            :current-parameter="currentParameter"
            :parameter-values="parameterValues"
            @back="goBack"
            @select-parameter="assignToParameter"
            @calculation-request="handleCalculate"
          />
        </transition>
      </div>
    </transition>
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
      this.$emit('menu-state', true)
    },
    goBack() {
      this.currentView = 'main'
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
      const missingParam = this.findMissingParameter()
      if (!missingParam) return

      this.currentParameter = {
        key: missingParam,
        label: this.getParameterLabel(missingParam)
      }
      
      try {
        const result = await this.calculate()
        if (result) {
          this.parameterValues[result.parameter] = String(result.value)
          this.$emit('parameter-update', this.parameterValues)
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
      
      const filledParams = requiredParams.filter(param => 
        params[param] !== '' && params[param] !== undefined
      ).length

      if (filledParams !== 4) return null

      return requiredParams.find(param => 
        !params[param] || params[param] === ''
      )
    },
    async calculate() {
      if (this.currentView !== 'tvm') return null

      const params = Object.entries(this.parameterValues).reduce((acc, [key, value]) => {
        if (value !== '' && value !== undefined) {
          if (key === 'pv' || key === 'pmt') {
            acc[key] = -Number(value)
          } else if (key === 'fv' || key === 'i' || key === 'n') {
            acc[key] = Number(value)
          } else {
            acc[key] = value
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
  top: 50%;
  right: calc(50% - 160px);
  margin-right: -360px;
  transform: translateY(-50%);
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  min-width: 280px;
  max-height: 80vh;
  overflow-y: auto;
  padding: 0;
  backdrop-filter: blur(10px);
}

.main-menu {
  overflow: hidden;
}

.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  border-radius: 12px 12px 0 0;
}

.menu-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.close-button:hover {
  color: #2c3e50;
  background-color: rgba(0, 0, 0, 0.05);
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding: 16px;
}

/* Transitions */
.menu-enter-active,
.menu-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-enter-from {
  opacity: 0;
  transform: translate(20px, -50%);
}

.menu-leave-to {
  opacity: 0;
  transform: translate(-20px, -50%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.category-enter-active,
.category-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.category-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Scrollbar styling */
.menu-content::-webkit-scrollbar {
  width: 8px;
}

.menu-content::-webkit-scrollbar-track {
  background: #f8f9fa;
  border-radius: 4px;
}

.menu-content::-webkit-scrollbar-thumb {
  background-color: #ced4da;
  border-radius: 4px;
}

.menu-content::-webkit-scrollbar-thumb:hover {
  background-color: #adb5bd;
}
</style>