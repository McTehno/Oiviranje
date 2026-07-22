import {exec} from 'child_process';

function simulateSQLInjection(req, database) {
    const userId = req.query.id;
    const query = `SELECT * FROM users WHERE id = '${userId}'`;
    database.query(query);
}

function simulateCommandInjection(req) {
    const userInput = req.query.userInput;
    const command = `ls ${userInput}`;
    exec(command);
  
    // Simulate executing the command (in a real application, this would be sent to the shell)
    // For demonstration purposes, we just log the command
}
function simulateHQLInjection(req, session) {

    const userId = req.query.id;
    const query = `FROM User WHERE id = ${userId}`;
    session.createQuery(query);
    console.log("Executing HQL query:", query);
    // Simulate executing the HQL query (in a real application, this would be sent to the database)
    // For demonstration purposes, we just log the query
}