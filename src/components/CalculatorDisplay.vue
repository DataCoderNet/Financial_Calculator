<template>
  <div class="calculator-display">
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-else class="display-container">
      <div v-if="description" class="input-description">
        {{ description }}
      </div>
      <div class="display-value" :class="{ 'with-description': description }">
        {{ formatValue(value) }}
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
    }
  },
  methods: {
    formatValue(val) {
      // Remove trailing zeros after decimal point
      if (val.includes('.')) {
        return Number(val).toString()
      }
      return val
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
  text-align: right;
  min-height: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.display-container {
  display: flex;
  flex-direction: column;
}

.display-value {
  font-size: 2rem;
  font-weight: 500;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.display-value.with-description {
  font-size: 1.5rem;
}

.input-description {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 4px;
  text-align: left;
}

.error-message {
  color: #dc3545;
  font-size: 1rem;
}
</style>