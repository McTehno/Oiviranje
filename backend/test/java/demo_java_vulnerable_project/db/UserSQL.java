/*package test.java.demo_java_vulnerable_project.db;
import jakarta.servlet.http.HttpServletRequest;
public class UserSQL {
   public void find(HttpServletRequest request, java.sql.Statement statement) throws Exception {
        String id = request.getParameter("id");
        statement.executeQuery("SELECT * FROM users WHERE id = " + id);
    }
}*/


package test.java.demo_java_vulnerable_project.db;

import jakarta.servlet.http.HttpServletRequest;

import java.sql.Statement;

public class UserSQL {

    // 1. SQL Injection s konkatenacijo
    public void findUserById(HttpServletRequest request,Statement statement) throws Exception {
        String userId = request.getParameter("id");

        String query ="SELECT * FROM users WHERE id = " + userId;

        statement.executeQuery(query);
    }


    // 2. SQL Injection z uporabnikovim e-poštnim naslovom
    public void findUserByEmail(HttpServletRequest request,Statement statement) throws Exception {
        String email = request.getParameter("email");

        String query ="SELECT * FROM users WHERE email = '" + email + "'";

        statement.executeQuery(query);
    }


    // 3. SQL Injection z uporabo String.format()
    public void findUserByUsername(HttpServletRequest request,Statement statement) throws Exception {
        String username = request.getParameter("username");

        String query = String.format("SELECT * FROM users WHERE username = '%s'",username);

        statement.executeQuery(query);
    }


    // 4. SQL Injection z uporabo StringBuilder
    public void findUserByRole(HttpServletRequest request, Statement statement) throws Exception {
        String role = request.getParameter("role");

        String query = new StringBuilder().append("SELECT * FROM users WHERE role = '").append(role).append("'").toString();

        statement.executeQuery(query);
    }


    // 5. Neposreden uporabniški vhod v SQL-poizvedbi
    public void findUserDirectly( HttpServletRequest request,Statement statement) throws Exception {
        statement.executeQuery("SELECT * FROM users WHERE id = "+ request.getParameter("id"));
    }


    // 6. SQL Injection v pogoju LIKE
    public void searchUsers(HttpServletRequest request,Statement statement    )  throws Exception {
        String search = request.getParameter("search");

        String query ="SELECT * FROM users "+ "WHERE username LIKE '%" + search + "%'";

        statement.executeQuery(query);
    }


    // 7. SQL Injection v ORDER BY
    public void sortUsers(HttpServletRequest request,Statement statement) throws Exception {
        String sortField = request.getParameter("sort");

        String query ="SELECT * FROM users ORDER BY " + sortField;

        statement.executeQuery(query);
    }
}