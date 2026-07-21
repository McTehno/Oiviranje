package test.java.demo_java_vulnerable_project.safe;

public class SafeExamples {
    public void safeSql(java.sql.PreparedStatement statement, String id) throws Exception {
        statement.setString(1, id);
        statement.executeQuery();
    }
}
