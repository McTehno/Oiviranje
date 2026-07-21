export async function findUserByName(req, sequelize) {
  const name = req.body.name;
  return sequelize.query(`FROM User u WHERE u.name = '${name}'`);
}