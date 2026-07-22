export async function findUserProfile(req, users) {
 const filter = req.body.filter;
  const operator = req.query.operator;
  return users.findOne({ name: filter, enabled: { $ne: operator } });    
}