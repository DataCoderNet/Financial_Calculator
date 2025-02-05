<template>
  <div class="tvm-menu">
    <div class="menu-header">
      <h3>Time Value of Money</h3>
      <button class="back-button" @click="$emit('back')">&larr; Back</button>
    </div>
    <div class="function-grid">
      <CalculatorButton
        v-for="func in tvmFunctions"
        :key="func.key"
        :label="func.label"
        type="fin"
        @click="selectFunction(func)"
      />
    </div>
  </div>
</template>

<script>
import CalculatorButton from '../CalculatorButton.vue'

export default {
  name: 'TVMMenu',
  components: {
    CalculatorButton
  },
  data() {
    return {
      tvmFunctions: [
        { key: 'n', label: 'N', description: 'Number of periods' },
        { key: 'i', label: 'I%YR', description: 'Annual interest rate' },
        { key: 'pv', label: 'PV', description: 'Present value' },
        { key: 'pmt', label: 'PMT', description: 'Payment amount' },
        { key: 'fv', label: 'FV', description: 'Future value' },
        { key: 'pyr', label: 'P/YR', description: 'Payments per year' },
        { key: 'end', label: 'END', description: 'Payment timing (End of period)' }
      ]
    }
  },
  methods: {
    selectFunction(func) {
      this.$emit('select-function', {
        type: 'tvm',
        function: func.key,
        label: func.label,
        description: func.description
      })
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
  max-width: 320px;
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

.function-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.function-grid :deep(.calculator-button) {
  width: 100%;
  height: 40px;
  font-size: 1rem;
}
</style>