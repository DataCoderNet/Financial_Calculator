<template>
  <div class="tvm-menu">
    <div class="tvm-header">
      <button class="back-button" @click="$emit('back')">&larr;</button>
      <h3>Time Value of Money</h3>
      <button class="close-button" @click="$emit('back')">&times;</button>
    </div>
    <div class="parameter-buttons">
      <button 
        v-for="param in parameterButtons" 
        :key="param.key"
        class="param-button"
        :class="{ 'calculated': lastCalculated === param.key }"
        @click="handleParameterClick(param)"
      >
        {{ param.label }}
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
      lastCalculated: '',
      parameterButtons: [
        { key: 'n', label: 'N' },
        { key: 'i', label: 'I%YR' },
        { key: 'pv', label: 'PV' },
        { key: 'pmt', label: 'PMT' },
        { key: 'fv', label: 'FV' }
      ]
    }
  },
  methods: {
    handleParameterClick(param) {
      this.$emit('select-parameter', param)
    }
  }
}
</script>

<style scoped>
.tvm-menu {
  width: 320px;
}

.tvm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  background-color: #f8f9fa;
}

.tvm-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
  flex: 1;
  text-align: center;
}

.back-button,
.close-button {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #666;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.back-button:hover,
.close-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: #333;
}

.parameter-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
}

.param-button {
  padding: 12px;
  font-size: 1rem;
  color: #333;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}

.param-button:hover {
  background-color: #e3f2fd;
  border-color: #2196f3;
  color: #1976d2;
}

.param-button.calculated {
  background-color: #e8f5e9;
  border-color: #4caf50;
  color: #2e7d32;
}
</style>