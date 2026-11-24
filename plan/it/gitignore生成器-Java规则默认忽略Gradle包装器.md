# Java 模板默认忽略 Gradle 包装器

- 受影响工具：`tools/it/gitignore-generator.html`
- 问题：Java/Kotlin 模板包含无例外的 `*.jar`，会匹配项目常需提交的 `gradle/wrapper/gradle-wrapper.jar`。新项目使用生成规则后可能无法提交包装器，影响其他开发者运行构建。源码分析，需用 `git check-ignore` 复核具体路径。
- 解决方案：对 Gradle 包装器添加明确例外，或改为忽略明确的构建产物目录，并提示检查项目是否需要跟踪其他 JAR；验证包装器可跟踪且构建产物仍被忽略。
