<template>
  <div class="icnv-menu">
    <div class="menu-header">
      <h3>Interest Conversion</h3>
      <button class="back-button" @click="$emit('back')">&larr; Back</button>
    </div>

    <div class="parameters-grid">
      <!-- Rate Input -->
      <div 
        :class="['parameter-item', { active: isActive(selectedParameter) }]"
        @click="selectParameter('rate', 'Rate')"
      >
        <div class="param-label">Rate (%)</div>
        <div class="param-value">{{ formatValue(parameters.rate) }}</div>
      </div>

      <!-- Compounding Periods Selection -->
      <div class="parameter-item">
        <div class="param-label">Periods/Year</div>
        <select v-model="parameters.periods" class="periods-select">
          <option value="1">Annual (1)</option>
          <option value="2">Semi-annual (2)</option>
          <option value="4">Quarterly (4)</option>
          <option value="12">Monthly (12)</option>
          <option value="365">Daily (365)</option>
        </select>
      </div>
    </div>

    <!-- Conversion Direction -->
    <div class="conversion-direction">
      <label class="radio-label">
        <input 
          type="radio" 
          v-model="parameters.conversionType" 
          value="nominal-to-effective"
        > Nominal to Effective
      </label>
      <label class="radio-label">
        <input 
          type="radio" 
          v-model="parameters.conversionType" 
          value="effective-to-nominal"
        > Effective to Nominal
      </label>
    </div>

    <!-- Calculate Button -->
    <div class="calculate-section">
      <button 
        class="calculate-button"
        @click="calculate"
        :disabled="!canCalculate"
      >
        Convert
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ICNVMenu',
  emits: ['back', 'select-parameter', 'calculation-request'],
  data() {
    return {
      parameters: {
        rate: '',
        periods: '12',
        conversionType: 'nominal-to-effective'
      },
      selectedParameter: null
    }
  },
  computed: {
    canCalculate() {
      // Should be able to calculate if we have a rate and periods are selected (which has a default)
      return this.parameters.rate !== '' && this.parameters.rate !== undefined
    }
  },
  methods: {
    selectParameter(key, label) {
      this.selectedParameter = { key, label }
      this.$emit('select-parameter', { key: 'rate', label: 'Rate%' })
    },
    isActive(param) {
      return this.selectedParameter?.key === param.key
    },
    formatValue(value) {
      if (!value && value !== 0) return '?'
      
      if (typeof value === 'string' && !isNaN(value)) {
        const num = Number(value)
        if (Number.isInteger(num)) {
          return num.toString()
        }
        return num.toFixed(Math.min(4, value.split('.')[1]?.length || 0))
      }
      
      return value.toString()
    },
    async calculate() {
      if (!this.canCalculate) return
      
      try {
        // Parameters need to be in the right format for the API
        const params = {
          rate: Number(this.parameters.rate),
          compounding_periods: Number(this.parameters.periods)
        }

        // Call the appropriate endpoint based on conversion type
        const endpoint = this.parameters.conversionType || 'nominal-to-effective'
        const response = await fetch(`http://localhost:8000/api/fin/icnv/${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(params)
        })

        if (!response.ok) {
          throw new Error('Conversion failed')
        }

        const result = await response.json()
        
        // Emit the result with the appropriate parameter label
        const resultLabel = endpoint === 'nominal-to-effective' ? 'EFF%' : 'NOM%'
        this.$emit('calculation-request', {
          value: result.value,
          parameter: resultLabel
        })

        // Reset for next calculation
        this.selectedParameter = null
      } catch (error) {
        console.error('Failed to convert:', error)
      }
    }
  }
}
</script>

<style scoped>
.icnv-menu {
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

.periods-select {
  width: 100%;
  margin-top: 4px;
  padding: 4px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.conversion-direction {
  margin: 15px 0;
  padding: 15px;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.radio-label {
  display: block;
  margin: 8px 0;
  font-size: 0.9rem;
  color: #333;
}

.calculate-section {
  margin-top: 15px;
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