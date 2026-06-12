import { useState } from 'react'
import Layout from './Layout'
import Home from './Home'
import Explore from './Explore'
import MovieDetail from './MovieDetail'
import Watch from './Watch'
import Dashboard from './Dashboard'
import Profile from './Profile'
import Subscription from './Subscription'
import Login from './Login'
import Register from './Register'
import AdminDashboard from './AdminDashboard'

function App() {
  const data = window.CineVerseData || { page: 'home', user: '', csrfToken: '', payload: {} };
  const { page, user, userAvatar, userEmail, isSuperuser, csrfToken, payload } = data;

  const renderPage = () => {
    switch (page) {
      case 'home':
        return <Home payload={payload} user={user} csrfToken={csrfToken} />;
      case 'login':
        return <Login payload={payload} user={user} csrfToken={csrfToken} />;
      case 'register':
        return <Register payload={payload} user={user} csrfToken={csrfToken} />;
      case 'dashboard':
        return <Dashboard payload={payload} user={user} csrfToken={csrfToken} />;
      case 'movie_list':
      case 'search_results':
        return <Explore payload={payload} user={user} csrfToken={csrfToken} page={page} />;
      case 'movie_detail':
        return <MovieDetail payload={payload} user={user} csrfToken={csrfToken} />;
      case 'watch':
        return <Watch payload={payload} user={user} csrfToken={csrfToken} />;
      case 'profile':
        return <Profile payload={payload} user={user} csrfToken={csrfToken} />;
      case 'subscription':
        return <Subscription payload={payload} user={user} csrfToken={csrfToken} />;
      case 'admin_dashboard':
        return <AdminDashboard payload={payload} user={user} csrfToken={csrfToken} />;
      default:
        return (
          <div className="pt-32 text-center text-white">
            <h1 className="text-3xl font-bold">404 - Page Not Found</h1>
            <p className="text-on-surface-variant mt-2">The requested page "{page}" is not supported.</p>
          </div>
        );
    }
  };

  return (
    <Layout
      user={user}
      userAvatar={userAvatar}
      userEmail={userEmail}
      isSuperuser={isSuperuser}
      csrfToken={csrfToken}
      page={page}
    >
      {renderPage()}
    </Layout>
  );
}

export default App
