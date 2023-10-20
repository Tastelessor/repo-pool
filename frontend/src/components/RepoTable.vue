<template>
  <el-table
    :data="tableData"
    style="width: 100%"
    :row-class-name="tableRowClassName"
  >
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="branch" label="Branch" width="200" />
    <el-table-column prop="url" label="Branch"/>
  </el-table>
</template>

<script lang="ts" setup>
interface Repo {
  name: string
  branch: string
  url: string
}

const tableRowClassName = ({
  row,
  rowIndex,
}: {
  row: Repo
  rowIndex: number
}) => {
  if (rowIndex === 1) {
    return 'warning-row'
  } else if (rowIndex === 3) {
    return 'success-row'
  }
  return ''
}

const tableData: Repo[] = [
  {
    name: 'soakit-ui',
    branch: 'develop',
    url: 'baidu.com'
  },
  {
    name: 'soakit-ui',
    branch: 'develop',
    url: 'baidu.com'
  },
  {
    name: 'soakit-ui',
    branch: 'develop',
    url: 'baidu.com'
  },
  {
    name: 'soakit-ui',
    branch: 'develop',
    url: 'baidu.com'
  },
  {
    name: 'soakit-ui',
    branch: 'develop',
    url: 'baidu.com'
  },
  {
    name: 'soakit-ui',
    branch: 'develop',
    url: 'baidu.com'
  },
  {
    name: 'soakit-ui',
    branch: 'develop',
    url: 'baidu.com'
  },
]
</script>

<style>
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>