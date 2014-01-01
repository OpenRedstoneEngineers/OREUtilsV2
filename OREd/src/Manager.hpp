/**
 *  ORE Server management daemon
 *  Copyright (C) 2013 OpenRedstone
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef _ORED_MANAGER_
#define _ORED_MANAGER_

#include "ProtoServer.hpp"

#include "Console.hpp"

#include <map>
#include <string>

namespace OREd
{
	/**
	 * \brief Encapsulates a console pointer.
	 */
	class ConsolePtr
	{
	public:
		ConsolePtr() : m_Ptr(NULL) {}

		ConsolePtr(Console* ptr) : m_Ptr(ptr) {}

		ConsolePtr(const std::string& path, char* const* argv);

		/**
		 * \brief Stop the child process.
		 */
		void Stop();

		/**
		 * \brief (Re)start the child process.
		 */
		void Start();

		/**
		 * \return the internal pointer.
		 */
		Console* GetPtr();

		inline Console& operator*() const { return *m_Ptr; }
		inline Console* operator->() const { return m_Ptr; }

	protected:
		Console* m_Ptr;

		std::string m_Path;

		char* const* m_Argv;
	};

	/**
	 * \brief Manages the server consoles.
	 */
	class Manager : public ProtoServer
	{
	public:
		typedef bool (*CmdHandler)(Client* cli, ConsolePtr& target, const ArgsList& args);

		typedef std::map<const std::string, ConsolePtr*> ConsoleMap;

		typedef std::map<const std::string, CmdHandler> HandlerMap;

	public:
		Manager(const int port, const std::string& name) : ProtoServer(port), m_Host(name) {}

		/**
		 * \brief Init a console instance.
		 */
		void InitConsole(const std::string& name, ConsolePtr* console);

		/**
		 * \return the console with the specified name.
		 */
		ConsolePtr* GetConsole(const std::string& name);

		/**
		 * \return the associated hostname.
		 */
		std::string GetHostname() const;

	protected:
		ConsolePtr* GetConsoleByTarget(const std::string& target);

	protected:
		virtual bool OnCommand(Client* cli, const ArgsList& args);

		virtual bool OnEvent(Client* cli, const ArgsList& args);

		virtual bool OnQuery(Client* cli, const ArgsList& args);

	protected:
		/** Associated consoles */
		ConsoleMap m_Consoles;

		/** Command handlers */
		HandlerMap m_CmdHandlers;

		/** Query handlers */
		HandlerMap m_QueryHandlers;

		/** Associated host name */
		std::string m_Host;
	};

	inline Console* ConsolePtr::GetPtr()
	{
		return m_Ptr;
	}

	inline std::string Manager::GetHostname() const
	{
		return m_Host;
	}
} /* OREd */

#endif
