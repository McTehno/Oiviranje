package test.java.demo_java_vulnerable_project.system;
import jakarta.servlet.http.HttpServletRequest;

public class CommandTools {
    public void ping(HttpServletRequest request) throws Exception {
        String host = request.getParameter("host");
        new ProcessBuilder("sh", "-c", "ping " + host).start();
    }
}
