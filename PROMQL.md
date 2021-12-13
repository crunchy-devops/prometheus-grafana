# PromQL


```yaml
name: node.rules
  rules:
    - alert: DiskWillFillIn4Hours
      expr: predict_linear(node_filesystem_free{job="node"}[1h], 4 * 3600) < 0
      for: 5m
      labels:
      severity: page
```

## Disk full 
```yaml
- alert: OutOfDiskSpace
  expr: node_filesystem_free_bytes{mountpoint ="/rootfs"} / node_filesystem_size_bytes{mountpoint ="/rootfs"} * 100 < 10
  for: 15m
  labels:
  severity: warning
  annotations:
  summary: "Out of disk space (instance {{ $labels.instance }})"
  description: "Disk is almost full (< 10% left)\n  VALUE = {{ $value }}\n  LABELS: {{ $labels }}"
```



## Add file every 10 minutes
fallocate -l 10G foo
fallocate -l 10G foo1
fallocate -l 10G foo2
