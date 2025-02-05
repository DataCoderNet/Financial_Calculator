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

    <div class="function-info">
      <div class="sign-convention">
        <small>Cash Flow Convention:</small>
        <ul>
          <li>Money received (FV): positive (+)</li>
          <li>Money paid out (PV, PMT): negative (-)</li>
        </ul>
      </div>
      <div v-if="currentParameter" class="parameter-info">
        <div class="info-header">{{ currentParameter.label }}</div>
        <div class="info-description">{{ currentParameter.description }}</div>
      </div>
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
  methods: {
    handleParameterClick(func) {
      // Check if this parameter should be calculated
      if (this.canCalculateParameter(func)) {
        this.$emit('calculate-parameter', func)
      } else {
        this.$emit('select-parameter', func)
      }
    },
    canCalculateParameter(func) {
      const params = this.parameterValues
      
      // Define required parameters for each calculation
      const requiredParams = {
        pv: ['n', 'i', 'fv'],
        fv: ['n', 'i', 'pv'],
        n: ['pv', 'i', 'fv'],
        i: ['n', 'pv', 'fv'],
        pmt: ['n', 'i', 'pv', 'fv']
      }
      
      const required = requiredParams[func.key]
      if (!required) return false

      // Check if all required parameters except the current one are filled
      const hasRequiredParams = required.every(param => 
        !!params[param] && params[param] !== ''
      )
      
      // Check if current parameter is empty
      const isCurrentEmpty = !params[func.key] || params[func.key] === ''

      // Return true if we have all required params and current is empty
      return hasRequiredParams && isCurrentEmpty
    },
    isActive(func) {
      return this.currentParameter?.key === func.key
    },
    formatParameterValue(key) {
      const value = this.parameterValues[key]
      if (key === 'end') {
        return this.parameterValues[key] ? 'END' : 'BEG'
      }
      if (!value && value !== 0) return '?'
      return value.toString()
    }
  },
  watch: {
    // Watch for changes in parameter values
    parameterValues: {
      deep: true,
      handler(newValues) {
        // Find any parameter that can be calculated
        const calculableParam = this.tvmFunctions.find(func => 
          this.canCalculateParameter(func)
        )
        
        if (calculableParam) {
          this.$emit('calculate-parameter', calculableParam)
        }
      }
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

.function-info {
  margin-top: 15px;
  padding: 10px;
  background-color: #e9ecef;
  border-radius: 4px;
}

.sign-convention {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 10px;
}

.sign-convention ul {
  margin: 5px 0;
  padding-left: 20px;
}

.sign-convention li {
  margin: 2px 0;
}

.parameter-info {
  border-top: 1px solid #dee2e6;
  padding-top: 10px;
  margin-top: 10px;
}

.info-header {
  font-weight: bold;
  margin-bottom: 5px;
}

.info-description {
  font-size: 0.9rem;
  color: #666;
}
</style>