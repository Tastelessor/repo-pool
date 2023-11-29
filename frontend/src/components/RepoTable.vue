<template>
  <el-table
    :data="repos_table"
    style="width: 100%"
    :row-class-name="tableRowClassName"
  >
    <el-table-column prop="name" label="Name" width="150" />
    <el-table-column prop="dir" label="Dir" width="120" />
    <el-table-column prop="type" label="Type" width="60" />
    <el-table-column prop="branch" label="Branch" width="200" />
    <el-table-column prop="url" label="URL">
      <template #default="{ row }">
        <a :href="provied_real_url(row)" target="_blank"> {{ row.url }}</a>
      </template>
    </el-table-column>
    <el-table-column prop="compile_cmd" label="Compilation Command"/>
  </el-table>
</template>

<script lang="ts" setup>
import { ElNotification } from 'element-plus';
import { ref, onMounted, inject, reactive, onUnmounted } from 'vue'
import { global_socket, global_hl_branch } from '@/main';

const socket = inject("SOCKET", global_socket)

/**
 * Request repos info from backend
 */
interface Repo {
  name: string
  dir: string
  type: string
  branch: string
  url: string
  compile_cmd: string
}
const repos_json = ref(null)
const repos_table = ref<Repo[]>([])

function request_repos() {
  console.log("Request Repos")
  socket.value.emit("request_repos")
  socket.value.once("request_repos_ret", (ret:string) => {
    repos_json.value = JSON.parse(ret)
    parse_received_repos()
  })
}

function parse_received_repos() {
  console.log("Parse received repos")
  if (repos_json.value != null) {
    Object.values(repos_json.value).forEach(item => {
      console.log(repos_table)
      let item_temp: Repo = {
        name: "",
        dir: "",
        type: "",
        branch: "develop",
        url: "",
        compile_cmd: ""
      }
      Object.keys(item).forEach(key => {
        if (key in item_temp) {
          item_temp[key] = item[key]
        }
      })
      item_temp.dir = item["name"]
      if (item["type"] === "repo") {
        repos_table.value.push(item_temp)
      } 
      else if (item["type"] === "git") {
        // add each repo in git["repos"] to repos_table one by one
        item["repos"].forEach(git_item => {
          let git_item_temp = Object.create(item_temp)
          Object.keys(git_item).forEach(git_item_key => {
            if (git_item_key in git_item_temp) {
              // set default value for existing keys
              git_item_temp[git_item_key] = git_item[git_item_key]
            }
            // git name shall be parsed from url
            git_item_temp.name = extract_name_from_url(git_item["url"])
          })
          repos_table.value.push(git_item_temp)
        })
      } 
      else {
        ElNotification({
          title: '来自伟大的先知',
          message: '你该好好检查一下自己的json配置文件,写的什么玩意儿',
          type: 'error',
        })
      }
    })
  }
}

// Extract repository name from the given git url
function extract_name_from_url(url: string) {
  const last_slash_index = url.lastIndexOf('/')
  const git_name = url.slice(last_slash_index + 1)
  return git_name.slice(0, -4)
}

/**
 * Highlight the selected branch
 */
const selected_branch = inject("HL_BRANCH", global_hl_branch)
const tableRowClassName = ({
  row
}: {
  row: Repo
}) => {
  if (row.branch === selected_branch.value) {
    return 'success-row'
  }
  return ''
}

/**
 * Make url jumpable
 */
const provied_real_url = (row:Repo) => {
  let url:string = row.url
  if (url.startsWith("http")) {
    console.log("This is cloned by http")
  }
  else {
    console.log("This is cloned by ssh")
    url = url.slice(4)
    url = url.replace(':', '/')
    url = "https://" + url
  }
  return url
}
onMounted(() => {
  repos_table.value = []
  request_repos()
})
</script>

<style>
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>