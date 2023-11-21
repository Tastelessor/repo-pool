<template>
  <el-row>
    <el-col :span="6">
        <div class="statistic-card">
          <el-countdown
          title="仓库&索引更新倒计时"
          format="HH:mm:ss"
          :value="sync_countdown"
        />
      </div>
    </el-col>
    <el-col :span="6">
      <div class="statistic-card">
        <el-statistic :value="statistics.git_project_num+statistics.repo_project_num" title="New transactions today">
          <template #title>
            <div style="display: inline-flex; align-items: center">
              当前仓库总量
            </div>
          </template>
        </el-statistic>
        <div class="statistic-footer">
          <div class="footer-item">
            <span>than yesterday</span>
            <span class="red">
              ↑16%
              <el-icon>
                <CaretTop />
              </el-icon>
            </span>
          </div>
          <div class="footer-item">
            <el-icon :size="14">
              <ArrowRight />
            </el-icon>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="statistic-card">
        <el-statistic :value="statistics.last_update_timecost" :precision="2" title="New transactions today">
          <template #title>
            <div style="display: inline-flex; align-items: center">
              上次更新耗时(mins)
            </div>
          </template>
        </el-statistic>
        <div class="statistic-footer">
          <div class="footer-item">
            <span>相比昨日</span>
            <span class="green">
              ↓16%
              <el-icon>
                <CaretTop />
              </el-icon>
            </span>
          </div>
          <div class="footer-item">
            <el-icon :size="14">
              <ArrowRight />
            </el-icon>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="statistic-card">
        <el-statistic :value="statistics.average_update_timecost" :precision="2" title="New transactions today">
          <template #title>
            <div style="display: inline-flex; align-items: center">
              平均更新耗时(mins)
            </div>
          </template>
        </el-statistic>
        <div class="statistic-footer">
          <div class="footer-item">
            <span>相比昨日</span>
            <span class="green">
              ↓1%
              <el-icon>
                <CaretTop />
              </el-icon>
            </span>
          </div>
          <div class="footer-item">
            <el-icon :size="14">
              <ArrowRight />
            </el-icon>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { ref, onMounted, inject, reactive } from 'vue'
import dayjs from 'dayjs'
import { global_socket } from '@/main';
import { Calendar } from '@element-plus/icons-vue'

const socket = inject("SOCKET", global_socket)

const value = ref(Date.now() + 1000 * 60 * 60 * 7)
const value2 = ref(dayjs().add(1, 'month').startOf('month'))

// Upper data board
const settings = reactive({
  workpath: "WORKPATH",
  repo_cfg_path: "REPO_CFG_PATH",
  sync_time:"02:00"
})

interface Map {
  [key:string]: any
  [index:number]:any
}

const statistics = reactive({
  synchronisation_times: 0,
  dir_count: 0,
  repo_project_num: 0,
  git_project_num: 0,
  last_update_timecost: 0,
  average_update_timecost: 0
}) as Map

const repo_cfg = ref(null)

/**
 * Init countdown
 */
const sync_countdown = ref(Date.now() + 1000 * 60 * 60 * 24 * 2)
function init_countdown() {
  const sync_time = new Date()
  const settings_tmp = sessionStorage.getItem('settings')
  if (settings_tmp !== null){
    settings.sync_time =  JSON.parse(settings_tmp)["sync_time"]
  }
  const [hours, mins] = settings.sync_time.split(":").map(Number)
  if (sync_time.getHours() >= hours && sync_time.getMinutes() >= mins) {
    sync_time.setHours(hours, mins, 0, 0)
    sync_time.setDate(sync_time.getDate() + 1)
  }
  else {
    sync_time.setHours(hours, mins, 0, 0)
    sync_time.setDate(sync_time.getDate())
  }
  sync_countdown.value = sync_time.getTime()
}

/**
 * Init statistics
 */
function request_statistics() {
  console.log("Request statistics")
  socket.value.emit("request_statistics")
  socket.value.once("request_statistics_ret", (ret:string) => {
    const parsed_ret = JSON.parse(ret)
    console.log(parsed_ret)
    sessionStorage.setItem('statistics', ret)
    Object.keys(parsed_ret).forEach(key => {
      if (key in statistics) {
        statistics[key] = parsed_ret[key]
      }
    })
  })
  console.log("last update:", statistics.last_update_timecost)
}

onMounted(() => {
  init_countdown()
  request_statistics()
})
</script>

<style scoped>
.el-col {
  text-align: center;
}

.countdown-footer {
  margin-top: 8px;
}

:global(h2#card-usage ~ .example .example-showcase) {
  background-color: var(--el-fill-color) !important;
}

.el-statistic {
  --el-statistic-content-font-size: 28px;
}

.statistic-card {
  height: 100%;
  padding: 20px;
  border-radius: 4px;
  background-color: var(--el-bg-color-overlay);
}

.statistic-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--el-text-color-regular);
  margin-top: 16px;
}

.statistic-footer .footer-item {
  display: flex;
  justify-content: center;
  align-items: center;
}

.statistic-footer .footer-item span:last-child {
  display: inline-flex;
  align-items: center;
  margin-left: 4px;
}

.green {
  color: var(--el-color-success);
}
.red {
  color: var(--el-color-error);
}
</style>
