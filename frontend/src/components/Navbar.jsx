import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogOut, Database, History, Home } from 'lucide-react';
import { useAuth } from '../utils/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 glass-effect border-b border-white/10"
    >
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3 group">
            <motion.div
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.6 }}
              className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center glow-effect"
            >
              <Database className="w-6 h-6 text-white" />
            </motion.div>
            <div>
              <h1 className="text-2xl font-display font-bold text-gradient">
                ChemViz Pro
              </h1>
              <p className="text-xs text-blue-300/60">Equipment Analytics Platform</p>
            </div>
          </Link>

          {isAuthenticated && (
            <div className="flex items-center space-x-6">
              <Link to="/dashboard">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg glass-effect hover:bg-white/10 transition-all"
                >
                  <Home className="w-4 h-4" />
                  <span className="font-medium">Dashboard</span>
                </motion.button>
              </Link>

              <Link to="/history">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg glass-effect hover:bg-white/10 transition-all"
                >
                  <History className="w-4 h-4" />
                  <span className="font-medium">History</span>
                </motion.button>
              </Link>

              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <p className="text-sm font-medium">{user?.username}</p>
                  <p className="text-xs text-blue-300/60">{user?.email}</p>
                </div>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleLogout}
                  className="p-3 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 transition-all"
                >
                  <LogOut className="w-5 h-5 text-red-400" />
                </motion.button>
              </div>
            </div>
          )}
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;