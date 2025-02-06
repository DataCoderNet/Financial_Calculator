<template>
  <div class="tvm-menu">
    <div class="menu-header">
      <h3>Time Value of Money</h3>
      <button class="back-button" @click="$emit('back')">&larr; Back</button>
    </div>

    <div class="parameters-grid">
      <transition-group name="parameter">
        <div 
          v-for="func in tvmFunctions" 
          :key="func.key"
          :class="['parameter-item', { active: isActive(func) }]"
          @click="handleParameterClick(func)"
        >
          <div class="param-label">{{ func.label }}</div>
          <transition name="value" mode="out-in">
            <div class="param-value" :key="parameterValues[func.key]">
              {{ formatParameterValue(func.key) }}
            </div>
          </transition>
        </div>
      </transition-group>
    </div>

    <!-- Calculate Button -->
    <div class="calculate-section">
      <transition name="slide">
        <div class="sign-convention" v-show="canCalculate">
          <small>Cash Flow Convention:</small>
          <ul>
            <li>Money received (FV): positive (+)</li>
            <li>Money paid out (PV, PMT): negative (-)</li>
          </ul>
        </div>
      </transition>
      <button 
        class="calculate-button"
        @click="requestCalculation"
        :disabled="!canCalculate"
      >
        Calculate
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TVMMenu',
  props: {
    currentParameter: {
      type: Object,
      default: null
    },
    parameterValues: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      tvmFunctions: [
        { key: 'n', label: 'N', description: 'Number of periods (years)' },
        { key: 'i', label: 'I%YR', description: 'Annual interest rate (as percentage)' },
        { key: 'pv', label: 'PV', description: 'Present value (negative for cash paid out)' },
        { key: 'pmt', label: 'PMT', description: 'Payment amount (negative for cash paid out)' },
        { key: 'fv', label: 'FV', description: 'Future value (positive for cash received)' },
        { key: 'pyr', label: 'P/YR', description: 'Payments per year (default: 12)' },
        { key: 'end', label: 'END', description: 'Payment timing (END or BEG)' }
      ]
    }
  },
  computed: {
    filledParameters() {
      return Object.entries(this.parameterValues)
        .filter(([key]) => key !== 'pyr' && key !== 'end')
        .filter(([, value]) => value !== '' && value !== undefined)
        .length
    },
    canCalculate() {
      // Need at least 3 parameters filled to calculate the 4th
      return this.filledParameters >= 3
    }
  },
  methods: {
    handleParameterClick(func) {
      this.$emit('select-parameter', func)
    },
    isActive(func) {
      return this.currentParameter?.key === func.key
    },
    formatParameterValue(key) {
      const value = this.parameterValues[key]
      
      // Special handling for end/pyr
      if (key === 'end') {
        return this.parameterValues[key] ? 'END' : 'BEG'
      }
      if (key === 'pyr') {
        return value || '12'
      }
      
      // Handle empty values
      if (!value && value !== 0) return '?'
      
      // Format numbers with 4 decimal places max
      if (typeof value === 'string' && !isNaN(value)) {
        const num = Number(value)
        if (Number.isInteger(num)) {
          return num.toString()
        }
        return num.toFixed(Math.min(4, value.split('.')[1]?.length || 0))
      }
      
      return value.toString()
    },
    requestCalculation() {
      if (!this.canCalculate) return
      this.$emit('calculation-request')
    }
  }
}
</script>

<style scoped>
.tvm-menu {
  background-color: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  width: 100%;
  min-width: 280px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.menu-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
  font-weight: 600;
}

.back-button {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 8px 12px;
  font-size: 1rem;
  border-radius: 6px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.back-button:hover {
  color: #2c3e50;
  background-color: rgba(0, 0, 0, 0.05);
}

.parameters-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.parameter-item {
  background-color: white;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.parameter-item:hover {
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.parameter-item.active {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

.param-label {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.param-value {
  font-size: 1.1rem;
  font-family: monospace;
  padding: 4px 0;
}

.calculate-section {
  margin-top: 20px;
  padding: 16px;
  background-color: #e9ecef;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sign-convention {
  font-size: 0.85rem;
  color: #495057;
  background-color: white;
  padding: 12px;
  border-radius: 6px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.sign-convention ul {
  margin: 8px 0;
  padding-left: 20px;
}

.sign-convention li {
  margin: 4px 0;
}

.calculate-button {
  width: 100%;
  padding: 12px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(40, 167, 69, 0.2);
}

.calculate-button:hover:not(:disabled) {
  background-color: #218838;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
}

.calculate-button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(40, 167, 69, 0.2);
}

.calculate-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  opacity: 0.75;
  transform: none;
  box-shadow: none;
}

/* Transitions */
.parameter-enter-active,
.parameter-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.parameter-enter-from,
.parameter-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.value-enter-active,
.value-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.value-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.value-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 200px;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
  margin-bottom: 0;
  padding: 0;
  overflow: hidden;
}
</style>