import React from 'react';
import { Navigate } from 'react-router-dom';

interface PublicRouteProps {
  children: React.ReactNode;
}

const PublicRoute: React.FC<PublicRouteProps> = ({ children }) => {
  const isAuthenticated = Boolean(localStorage.getItem('token')); // Replace with your auth logic

  return isAuthenticated ? <Navigate to="/dashboard" /> : <>{children}</>;
};

export default PublicRoute;
