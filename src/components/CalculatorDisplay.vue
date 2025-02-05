<template>
  <div class="calculator-display">
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-else class="display-container">
      <!-- TVM Parameters display -->
      <div v-if="parameters" class="parameters-display">
        <div 
          v-for="(value, key) in parameters" 
          :key="key"
          class="parameter-row"
          :class="{ 
            'active': isActiveParameter(key),
            'calculated': isLastCalculated(key)
          }"
        >
          <span class="param-label">{{ formatLabel(key) }}:</span>
          <span class="param-value">{{ formatValue(value) }}</span>
        </div>
      </div>
      <!-- Current input display -->
      <div class="current-input">
        <div v-if="description" class="input-description">
          {{ description }}
          <span v-if="isCalculatedValue" class="calculated-badge">Calculated</span>
        </div>
        <div class="display-value" :class="{ 'with-description': description }">
          {{ formatValue(value) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
    }
  },
  computed: {
    isCalculatedValue() {
      return this.calculatedParameter === this.description.split(' ')[1]
    }
  },
  methods: {
    formatValue(val) {
      if (!val && val !== 0) return '0'
      // Remove trailing zeros after decimal point
      if (String(val).includes('.')) {
        const num = Number(val)
        return num.toFixed(Math.min(4, String(val).split('.')[1].length))
      }
      return String(val)
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
  min-height: 200px;
  display: flex;
  flex-direction: column;
}

.display-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.parameters-display {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}

.parameter-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.parameter-row.active {
  background-color: #e3f2fd;
  font-weight: 500;
}

.parameter-row.calculated {
  background-color: #e8f5e9;
  font-weight: 500;
}

.param-label {
  font-size: 0.9rem;
  color: #666;
}

.param-value {
  font-size: 0.9rem;
  color: #333;
  font-family: monospace;
}

.current-input {
  text-align: right;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}

.input-description {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 4px;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calculated-badge {
  font-size: 0.8rem;
  background-color: #4caf50;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
}

.display-value {
  font-size: 2rem;
  font-weight: 500;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: monospace;
}

.display-value.with-description {
  font-size: 1.8rem;
}

.error-message {
  color: #dc3545;
  font-size: 1rem;
  padding: 10px;
  text-align: center;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}
</style>