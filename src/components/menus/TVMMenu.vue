<template>
  <div class="tvm-menu">
    <div class="menu-header">
      <h3>Time Value of Money</h3>
      <button class="back-button" @click="$emit('back')">&larr; Back</button>
    </div>

    <div class="parameters-grid">
      <div 
        v-for="func in tvmFunctions" 
        :key="func.key"
        :class="['parameter-item', { active: isActive(func) }]"
        @click="handleParameterClick(func)"
      >
        <div class="param-label">{{ func.label }}</div>
        <div class="param-value">
          {{ formatParameterValue(func.key) }}
        </div>
      </div>
    </div>

    <!-- Calculate Button -->
    <div class="calculate-section">
      <div class="sign-convention">
        <small>Cash Flow Convention:</small>
        <ul>
          <li>Money received (FV): positive (+)</li>
          <li>Money paid out (PV, PMT): negative (-)</li>
        </ul>
      </div>
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
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  width: 100%;
  min-width: 280px;
}

.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.menu-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.back-button {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 5px 10px;
  font-size: 1rem;
}

.back-button:hover {
  color: #333;
}

.parameters-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-bottom: 15px;
}

.parameter-item {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.parameter-item:hover {
  border-color: #007bff;
}

.parameter-item.active {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}

.param-label {
  font-weight: bold;
  font-size: 0.9rem;
}

.param-value {
  font-size: 1.1rem;
  margin-top: 4px;
  font-family: monospace;
}

.calculate-section {
  margin-top: 15px;
  padding: 15px;
  background-color: #e9ecef;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.sign-convention {
  font-size: 0.85rem;
  color: #666;
}

.sign-convention ul {
  margin: 5px 0;
  padding-left: 20px;
}

.sign-convention li {
  margin: 2px 0;
}

.calculate-button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.calculate-button:hover:not(:disabled) {
  background-color: #218838;
}

.calculate-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  opacity: 0.65;
}
</style>