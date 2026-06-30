<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div class="card budget-card">
      <label class="budget-label">{{ t('restocking.budget.label') }}</label>
      <div class="budget-input-row">
        <span class="budget-currency-symbol">$</span>
        <input
          v-model.number="budgetInput"
          type="number"
          min="0"
          step="100"
          :placeholder="t('restocking.budget.placeholder')"
          class="budget-input"
        />
      </div>
      <p class="budget-hint">{{ t('restocking.budget.hint') }}</p>
    </div>

    <div v-if="loading" class="loading-state">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>
    <div v-else>
      <div class="card summary-card">
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-label">{{ t('restocking.summary.itemsRecommended') }}</div>
            <div class="summary-value">{{ summaryData.items_recommended }}</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">{{ t('restocking.summary.totalEstimatedCost') }}</div>
            <div class="summary-value">{{ formatCurrency(summaryData.total_estimated_cost, currentCurrency) }}</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">{{ t('restocking.summary.budgetRemaining') }}</div>
            <div :class="['summary-value', budgetRemainingClass]">{{ budgetRemainingDisplay }}</div>
          </div>
        </div>
        <div v-if="activeBudget && summaryData.items_recommended > 0" class="budget-progress-container">
          <div class="budget-progress-track">
            <div
              class="budget-progress-fill"
              :class="{ 'over-budget': isOverBudget }"
              :style="{ width: budgetUsedPercent + '%' }"
            ></div>
          </div>
          <div class="budget-progress-labels">
            <span>{{ formatCurrency(summaryData.total_estimated_cost, currentCurrency) }}</span>
            <span>{{ formatCurrency(activeBudget, currentCurrency) }}</span>
          </div>
        </div>
      </div>

      <div v-if="sortedRecommendations.length === 0" class="empty-state">
        <div class="empty-icon">✓</div>
        <h3>{{ t('restocking.empty.title') }}</h3>
        <p>{{ t('restocking.empty.description') }}</p>
      </div>

      <div v-else class="card">
        <div class="card-header">
          <h3 class="card-title">
            {{ t('restocking.title') }}
            <span class="item-count">({{ sortedRecommendations.length }})</span>
          </h3>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.itemName') }}</th>
                <th>{{ t('restocking.table.category') }}</th>
                <th>{{ t('restocking.table.warehouse') }}</th>
                <th>{{ t('restocking.table.stock') }}</th>
                <th>{{ t('restocking.table.demandTrend') }}</th>
                <th>{{ t('restocking.table.recommendedQty') }}</th>
                <th>{{ t('restocking.table.estimatedCost') }}</th>
                <th class="sortable-header" @click="toggleSort">
                  {{ t('restocking.table.urgency') }}
                  <span class="sort-indicator">{{ sortAsc ? '↑' : '↓' }}</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in sortedRecommendations" :key="item.sku + item.warehouse">
                <td><strong>{{ item.sku }}</strong></td>
                <td>{{ translateProductName(item.name) }}</td>
                <td>{{ translateCategory(item.category) }}</td>
                <td>{{ translateWarehouse(item.warehouse) }}</td>
                <td class="stock-cell">
                  <span :class="['stock-qty', { 'stock-low': item.quantity_on_hand <= item.reorder_point }]">
                    {{ item.quantity_on_hand }}
                  </span>
                  <span class="stock-divider"> / </span>
                  <span class="stock-reorder">{{ item.reorder_point }}</span>
                </td>
                <td>
                  <span v-if="item.demand_trend" :class="['badge', item.demand_trend]">
                    {{ t(`trends.${item.demand_trend}`) }}
                  </span>
                  <span v-else class="text-muted">—</span>
                </td>
                <td><strong>{{ item.recommended_quantity }}</strong></td>
                <td>{{ formatCurrencyWithDecimals(item.estimated_cost, currentCurrency, 2) }}</td>
                <td>
                  <span :class="['badge', item.urgency]">
                    {{ t(`restocking.urgency.${item.urgency}`) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import { formatCurrency, formatCurrencyWithDecimals } from '../utils/currency'

const { t, currentCurrency, translateProductName, translateWarehouse } = useI18n()
const { selectedLocation, selectedCategory, getCurrentFilters } = useFilters()

const loading = ref(false)
const error = ref(null)
const budgetInput = ref(null)
const activeBudget = ref(null)
const summaryData = ref({
  budget: 0,
  total_estimated_cost: 0,
  items_recommended: 0,
  recommendations: []
})
const sortAsc = ref(false)

let debounceTimer = null

const URGENCY_ORDER = { critical: 0, high: 1, medium: 2, low: 3 }

const sortedRecommendations = computed(() => {
  const items = [...summaryData.value.recommendations]
  items.sort((a, b) => {
    const diff = URGENCY_ORDER[a.urgency] - URGENCY_ORDER[b.urgency]
    return sortAsc.value ? -diff : diff
  })
  return items
})

const isOverBudget = computed(() => {
  if (!activeBudget.value) return false
  return summaryData.value.total_estimated_cost > activeBudget.value
})

const budgetUsedPercent = computed(() => {
  if (!activeBudget.value || activeBudget.value === 0) return 0
  return Math.min((summaryData.value.total_estimated_cost / activeBudget.value) * 100, 100)
})

const budgetRemainingDisplay = computed(() => {
  if (!activeBudget.value) return t('restocking.summary.noBudgetSet')
  const remaining = activeBudget.value - summaryData.value.total_estimated_cost
  if (remaining < 0) {
    return '−' + formatCurrencyWithDecimals(Math.abs(remaining), currentCurrency.value, 0)
  }
  return formatCurrencyWithDecimals(remaining, currentCurrency.value, 0)
})

const budgetRemainingClass = computed(() => {
  if (!activeBudget.value) return 'summary-value-muted'
  return isOverBudget.value ? 'summary-value-danger' : 'summary-value-success'
})

const CATEGORY_I18N_KEYS = {
  'Circuit Boards': 'categories.circuitBoards',
  'Sensors': 'categories.sensors',
  'Actuators': 'categories.actuators',
  'Controllers': 'categories.controllers',
  'Power Supplies': 'categories.powerSupplies'
}

const translateCategory = (category) => {
  const key = CATEGORY_I18N_KEYS[category]
  return key ? t(key) : category
}

const toggleSort = () => {
  sortAsc.value = !sortAsc.value
}

const loadData = async () => {
  loading.value = true
  error.value = null
  try {
    const filters = getCurrentFilters()
    const data = await api.getRestockingRecommendations(
      activeBudget.value,
      filters.warehouse,
      filters.category
    )
    summaryData.value = data
  } catch (err) {
    error.value = t('restocking.error.loadFailed')
  } finally {
    loading.value = false
  }
}

watch(budgetInput, (val) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    activeBudget.value = (val && val > 0) ? val : null
    loadData()
  }, 600)
})

watch([selectedLocation, selectedCategory], () => {
  loadData()
})

onMounted(() => loadData())
</script>

<style scoped>
.budget-card {
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.budget-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.budget-input-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  max-width: 320px;
}

.budget-currency-symbol {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
}

.budget-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1.125rem;
  font-weight: 600;
  color: #0f172a;
  background: white;
  transition: border-color 0.2s;
}

.budget-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.budget-hint {
  font-size: 0.813rem;
  color: #94a3b8;
  margin: 0;
}

.summary-card {
  margin-bottom: 1.25rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  padding-bottom: 1rem;
}

.summary-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.375rem;
}

.summary-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.summary-value-muted {
  color: #94a3b8;
  font-size: 1rem;
  font-weight: 500;
  padding-top: 0.5rem;
}

.summary-value-success { color: #059669; }
.summary-value-danger { color: #dc2626; }

.budget-progress-container {
  padding-top: 0.75rem;
  border-top: 1px solid #f1f5f9;
}

.budget-progress-track {
  height: 8px;
  background: #e2e8f0;
  border-radius: 9999px;
  overflow: hidden;
}

.budget-progress-fill {
  height: 100%;
  background: #3b82f6;
  border-radius: 9999px;
  transition: width 0.4s ease;
}

.budget-progress-fill.over-budget { background: #dc2626; }

.budget-progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 0.375rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
}

.empty-icon {
  font-size: 3rem;
  color: #10b981;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.empty-state p { color: #64748b; font-size: 0.938rem; }

.loading-state, .error-state {
  padding: 2rem;
  text-align: center;
  color: #64748b;
}

.error-state { color: #dc2626; }

.stock-cell { white-space: nowrap; }
.stock-qty { font-weight: 700; color: #0f172a; }
.stock-qty.stock-low { color: #dc2626; }
.stock-divider { color: #94a3b8; }
.stock-reorder { color: #64748b; }
.text-muted { color: #94a3b8; }

.sortable-header { cursor: pointer; user-select: none; }
.sortable-header:hover { color: #2563eb; }
.sort-indicator { margin-left: 0.25rem; font-size: 0.75rem; }

.item-count {
  font-weight: 400;
  color: #64748b;
  font-size: 0.9em;
  margin-left: 0.25rem;
}

.badge.critical {
  background: #fee2e2;
  color: #7f1d1d;
  border: 1px solid #fca5a5;
}
</style>
