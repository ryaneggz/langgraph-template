import { TOKEN_NAME } from '@/config';
import React from 'react';
import { Navigate } from 'react-router-dom';

interface PublicRouteProps {
  children: React.ReactNode;
}

const PublicRoute: React.FC<PublicRouteProps> = ({ children }) => {
  const isAuthenticated = Boolean(localStorage.getItem(TOKEN_NAME)); // Replace with your token logic

  return isAuthenticated ? <Navigate to="/dashboard" /> : <>{children}</>;
};

export default PublicRoute;
