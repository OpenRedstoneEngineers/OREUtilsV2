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

#ifndef _ORED_CONSOLE_
#define _ORED_CONSOLE_

#include <string>

#include <sys/types.h>

namespace OREd
{
	/**
	 * \brief Represents a child process.
	 */
	class Console
	{
	public:
		Console(const std::string& path, char* const argv[]);

		~Console();

		/**
		 * \return whether the process is valid.
		 */
		bool IsValid() const;

		/**
		 * \return whether the process is running.
		 */
		bool IsRunning() const;

		/**
		 * \brief Read from the standard output of the process.
		 */
		bool Read(std::string& msg);

		/**
		 * \brief Write to the standard input of the process.
		 */
		bool Write(const std::string& msg);

		/**
		 * \brief Kill the process.
		 */
		void Kill();

	protected:
		/** Process handle */
		pid_t m_Handle;

		/** File descriptors */
		int m_PipeFd[2];
	};
} /* OREd */

#endif
