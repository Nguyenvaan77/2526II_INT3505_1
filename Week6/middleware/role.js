function authorizeRole(role) {
    return (req, res, next) => {
        if (req.user.role !== role) return res.sendStatus(403);
        next();
    };
}

function authorizeScope(scope) {
    return (req, res, next) => {
        if (!req.user.scopes.includes(scope)) return res.sendStatus(403);
        next();
    };
}

module.exports = { authorizeRole, authorizeScope };