### 获取平台列表

```bash
curl -X GET "{BASE_URL}/platforms"
```

此调用将返回支持的平台列表。

### 获取指定平台的语音角色

```bash
curl -X POST "{BASE_URL}/characters" \
     -H "Content-Type: application/json" \
     -d '{
           "platform": "{platform}",
           "token": "{token}"
         }'
```

此调用将返回指定平台的可用角色。请将 `{platform}` 和 `{token}` 替换为实际值。

### 获取情感列表（仅TTSON平台支持）

```bash
curl -X GET "{BASE_URL}/emotions" \
     -G --data-urlencode "platform={platform}"
```

此调用将返回指定平台的情感列表。请将 `{platform}` 替换为实际值。

### 文本转语音

```bash
curl -X POST "{BASE_URL}/tts" \
     -H "Content-Type: application/json" \
     -d '{
           "platform": "{platform}",
           "text": "这是一个测试文本",
           "character": "{character}",
           "token": "{token}",
           "options": {options}
         }'
```