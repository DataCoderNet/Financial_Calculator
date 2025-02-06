<template>
  <!-- Previous template code exactly as it was, only changing styles -->
  <div class="calculator-display" :class="{ 'expanded': isFinancialMode }">
    <transition name="fade" mode="out-in">
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-else key="display" class="display-container">
        <!-- TVM Parameters display -->
        <transition-group name="slide" tag="div" class="parameters-display" v-if="parameters && isFinancialMode">
          <div 
            v-for="(value, key) in filteredParameters" 
            :key="key"
            class="parameter-row"
            :class="{ 
              'active': isActiveParameter(key),
              'calculated': isLastCalculated(key)
            }"
          >
            <span class="param-label">{{ formatLabel(key) }}:</span>
            <transition name="number" mode="out-in">
              <span class="param-value" :key="value">{{ formatValue(value) }}</span>
            </transition>
          </div>
        </transition-group>
        <!-- Current input display -->
        <div class="current-input">
          <div class="input-description">
            <div v-if="description" class="description-text">
              {{ description }}
              <transition name="fade">
                <span v-if="isCalculatedValue" class="calculated-badge">Calculated</span>
              </transition>
            </div>
            <transition name="fade">
              <div v-if="memoryActive" class="memory-indicator">M</div>
            </transition>
          </div>
          <transition name="number" mode="out-in">
            <div class="display-value" :class="{ 'with-description': description }" :key="value">
              {{ formatValue(value) }}
            </div>
          </transition>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
// Script section remains exactly the same
export default {
  name: 'CalculatorDisplay',
  props: {
    value: {
      type: String,
      required: true
    },
    error: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    parameters: {
      type: Object,
      default: null
    },
    calculatedParameter: {
      type: String,
      default: ''
    },
    isFinancialMode: {
      type: Boolean,
      default: false
    },
    memoryActive: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isCalculatedValue() {
      return this.calculatedParameter === this.description.split(' ')[1]
    },
    filteredParameters() {
      if (!this.parameters) return {}
      
      const mainParams = ['n', 'i', 'pv', 'pmt', 'fv']
      return Object.fromEntries(
        Object.entries(this.parameters)
          .filter(([key]) => mainParams.includes(key))
      )
    }
  },
  methods: {
    formatValue(val) {
      if (!val && val !== 0) return '0'
      if (typeof val === 'string' && !val.trim()) return '0'
      
      try {
        const num = Number(val)
        
        if (isNaN(num)) return 'Error'
        if (!isFinite(num)) return num > 0 ? 'Overflow' : '-Overflow'
        
        if (Math.abs(num) >= 1e12) return num.toExponential(6)
        
        const parts = num.toString().split('.')
        const wholePart = parts[0]
        const decimalPart = parts[1] || ''
        
        const formattedWholePart = wholePart.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
        
        let formattedDecimalPart = ''
        if (decimalPart) {
          const minDecimals = this.isFinancialMode ? 2 : 0
          const maxDecimals = 4
          const decimals = Math.min(Math.max(decimalPart.length, minDecimals), maxDecimals)
          formattedDecimalPart = '.' + Number('0.' + decimalPart).toFixed(decimals).split('.')[1]
        } else if (this.isFinancialMode) {
          formattedDecimalPart = '.00'
        }
        
        return formattedWholePart + formattedDecimalPart
      } catch (e) {
        console.error('Number formatting error:', e)
        return String(val)
      }
    },
    formatLabel(key) {
      const labels = {
        n: 'N',
        i: 'I%YR',
        pv: 'PV',
        pmt: 'PMT',
        fv: 'FV',
        pyr: 'P/YR',
        end: 'END'
      }
      return labels[key] || key.toUpperCase()
    },
    isActiveParameter(key) {
      return this.description === `Enter ${key.toUpperCase()}`
    },
    isLastCalculated(key) {
      return key.toUpperCase() === this.calculatedParameter
    }
  }
}
</script>

<style scoped>
.calculator-display {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  height: 100px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.calculator-display.expanded {
  height: 320px; /* Increased height to show all parameters without scroll */
}

.display-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.parameters-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px; /* Increased gap between parameters */
  margin-bottom: 16px;
  padding: 16px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}

.parameter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px; /* Increased padding */
  border-radius: 4px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background-color: #f8f9fa;
}

.parameter-row.active {
  background-color: #e3f2fd;
  font-weight: 500;
  transform: scale(1.02);
}

.parameter-row.calculated {
  background-color: #e8f5e9;
  font-weight: 500;
  transform: scale(1.02);
}

.param-label {
  font-size: 1rem; /* Slightly larger font */
  color: #666;
  font-weight: 500;
}

.param-value {
  font-size: 1rem;
  color: #333;
  font-family: monospace;
  min-width: 100px; /* Increased min-width */
  text-align: right;
}

.current-input {
  text-align: right;
  padding: 12px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
  height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.input-description {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 24px;
}

.description-text {
  font-size: 0.9rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;
}

.calculated-badge {
  font-size: 0.8rem;
  background-color: #4caf50;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
}

.memory-indicator {
  font-size: 0.8rem;
  background-color: #2196f3;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: auto;
}

.display-value {
  font-size: 2rem;
  font-weight: 500;
  color: #333;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: monospace;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.display-value.with-description {
  font-size: 1.8rem;
}

.error-message {
  color: #dc3545;
  font-size: 1rem;
  padding: 12px;
  text-align: center;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}

.number-enter-active,
.number-leave-active {
  transition: all 0.2s ease;
}

.number-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.number-leave-to {
  transform: translateY(10px);
  opacity: 0;
}
</style>