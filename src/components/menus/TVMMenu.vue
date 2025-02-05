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
        @click="selectParameter(func)"
      >
        <div class="param-label">{{ func.label }}</div>
        <div class="param-value">{{ getParameterValue(func.key) }}</div>
      </div>
    </div>

    <div v-if="currentParameter" class="parameter-info">
      <div class="info-header">{{ currentParameter.label }}</div>
      <div class="info-description">{{ currentParameter.description }}</div>
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
        { key: 'pmt', label: 'PMT', description: 'Payment amount per period' },
        { key: 'fv', label: 'FV', description: 'Future value' },
        { key: 'pyr', label: 'P/YR', description: 'Payments per year (default: 12)' },
        { key: 'end', label: 'END', description: 'Payment timing (END or BEG)' }
      ]
    }
  },
  methods: {
    selectParameter(func) {
      this.$emit('select-parameter', func)
    },
    isActive(func) {
      return this.currentParameter?.key === func.key
    },
    getParameterValue(key) {
      if (key === 'end') {
        return this.parameterValues[key] ? 'END' : 'BEG'
      }
      return this.parameterValues[key] || '0'
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
}

.parameter-info {
  margin-top: 15px;
  padding: 10px;
  background-color: #e9ecef;
  border-radius: 4px;
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